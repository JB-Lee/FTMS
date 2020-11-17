import asyncio
import os
from typing import Optional

from ftms_lib import command, protocol, SessionContext
from ftms_lib.command import CommandType


class Client:
    class ClientListener(command.Listener):
        user: str
        pw: str

        def __init__(self, user: str, pw: str):
            self.user = user
            self.pw = pw

        def on_create(self, ctx: asyncio.transports.Transport):
            pass

        def on_close(self, ctx: asyncio.transports.Transport):
            pass

        def on_register(self, ctx: asyncio.transports.Transport):
            ctx.write(
                protocol.ProtocolBuilder()
                    .set_method("connect")
                    .set_session(None)
                    .set_params({"user": self.user,
                                 "pw": self.pw})
                    .build()
            )

        def on_receive(self, ctx: asyncio.transports.Transport, data: bytes):
            pass

        async def on_command(self, ctx: asyncio.transports.Transport, *args, **kwargs):
            pass

    class DataListener(ClientListener):
        command_ctx: asyncio.transports.Transport

        def __init__(self, command_ctx, user: str, pw: str):
            super(Client.DataListener, self).__init__(user, pw)
            self.command_ctx = command_ctx

        @command.command(method="sendFile_data", command_type=CommandType.CALL)
        async def send_file(self, ctx: asyncio.transports.Transport, header: dict, path: str, filename: str,
                            data: bytes, **kwargs):
            filepath = os.path.join(path, filename)

            success = False

            if os.path.exists(filepath) and os.path.isfile(filepath):
                # TODO 중복 파일 처리
                pass

            try:
                with open(filepath, "wb") as f:
                    f.write(data)
                    success = True

            except Exception as e:
                self.logger.critical(f"error: {e}")
                success = False

            finally:
                ctx.write(
                    protocol.ProtocolBuilder()
                        .set_method("sendFile_data")
                        .set_session(None)
                        .set_result({"header": header,
                                     "is_success": success})
                        .build()
                )

        @command.command(method="sendFile", command_type=CommandType.RESULT)
        async def send_file_result(self, ctx: asyncio.transports.Transport, header, is_success, **kwargs):
            raw_data = kwargs.get("raw")
            self.command_ctx.write(raw_data)

    class CommandListener(ClientListener):
        data_ctx: asyncio.transports.Transport

        def __init__(self, data_ctx, user: str, pw: str):
            super(Client.CommandListener, self).__init__(user, pw)
            self.data_ctx = data_ctx

        @command.command(method="listdir", command_type=CommandType.CALL)
        async def listdir(self, ctx: asyncio.transports.Transport, header: dict, path: str, **kwargs):
            ctx.write(
                protocol.ProtocolBuilder()
                    .set_method("listdir")
                    .set_session(None)
                    .set_result({"header": header,
                                 "dirs": os.listdir(path)})
                    .build()
            )

            print(path)

        @command.command(method="sendFile", command_type=CommandType.CALL)
        async def send_file(self, ctx: asyncio.transports.Transport, header: dict, src: dict, dst: dict, **kwargs):
            src_path = src.get("path")
            src_file_name = src.get("file_name")
            src_file_path = os.path.join(src_path, src_file_name)

            dst_path = dst.get("path")
            dst_file_name = dst.get("file_name")

            if os.path.exists(src_file_path) and os.path.isfile(src_file_path):
                with open(src_file_path, "rb") as f:
                    data = f.read()

                self.data_ctx.write(
                    protocol.ProtocolBuilder()
                        .set_method("sendFile_data")
                        .set_session(None)
                        .set_params({"header": header,
                                     "path": dst_path,
                                     "filename": dst_file_name,
                                     "data": data})
                        .build()
                )
            else:
                ctx.write(
                    protocol.ProtocolBuilder()
                        .set_method("sendFile")
                        .set_session(None)
                        .set_result({"header": header,
                                     "is_success": False})
                        .build()
                )

        @command.command(method="sendFile_data", command_type=CommandType.RESULT)
        async def send_file_result(self, ctx: asyncio.transports.Transport, header: dict, is_success: bool, **kwargs):
            ctx.write(
                protocol.ProtocolBuilder()
                    .set_method("sendFile")
                    .set_session(None)
                    .set_result({"header": header,
                                 "is_success": is_success})
                    .build()
            )


class Server:
    class ServerListener(command.Listener):
        connection: dict
        identifier: Optional[str]

        def on_create(self, ctx: asyncio.transports.Transport):
            pass

        def on_close(self, ctx: asyncio.transports.Transport):
            if self.identifier:
                if self.identifier in self.connection:
                    self.connection.pop(self.identifier)

        def on_register(self, ctx: asyncio.transports.Transport):
            pass

        def on_receive(self, ctx: asyncio.transports.Transport, data: bytes):
            pass

        async def on_command(self, ctx: asyncio.transports.Transport, *args, **kwargs):
            pass

        @classmethod
        def route(cls, client_id: str) -> asyncio.transports.Transport:
            transport = cls.connection.get(client_id)
            return transport

    class ClientCommandListener(ServerListener):
        connection: dict = dict()

        def __init__(self):
            self.identifier = None

        @command.command(method="connect", command_type=CommandType.CALL)
        async def connect(self, ctx, user, pw, **kwargs):
            self.identifier = user
            self.connection[user] = ctx

            ctx.write(
                protocol.ProtocolBuilder()
                    .set_method("connect")
                    .set_session(None)
                    .set_result({"is_success": True})
                    .build()
            )

        @command.command(method="sendFile", command_type=CommandType.RESULT)
        async def send_file_result(self, ctx, header: dict, is_success: bool, **kwargs):
            raw_data = kwargs.get("raw")
            app_id = header.get("requester")

            with SessionContext(Server.AppCommandListener.route(app_id)) as sess:
                sess.write(raw_data)

        @command.command(method="listdir", command_type=CommandType.RESULT)
        async def listdir_result(self, ctx, header: dict, dirs: list, **kwargs):
            raw_data = kwargs.get("raw")
            app_id = header.get("requester")

            with SessionContext(Server.AppCommandListener.route(app_id)) as sess:
                sess.write(raw_data)

    class AppCommandListener(ServerListener):
        connection: dict = dict()

        def register_session(self, ctx, session):
            self.identifier = session
            self.connection[session] = ctx

        @command.command(method="sendFile", command_type=CommandType.CALL)
        async def send_file(self, ctx, session, header: dict, src: dict, dst: dict, **kwargs):
            self.register_session(ctx, session)

            raw_data = kwargs.get("raw")
            client_id = header.get("from")

            sess = Server.ClientCommandListener.route(client_id)
            sess.write(raw_data)

        @command.command(method="listdir", command_type=CommandType.CALL)
        async def listdir(self, ctx, session, header: dict, path: str, **kwargs):
            self.register_session(ctx, session)

            raw_data = kwargs.get("raw")
            client_id = header.get("from")

            sess = Server.ClientCommandListener.route(client_id)
            sess.write(raw_data)

    class DataListener(ServerListener):
        connection: dict = dict()

        @command.command(method="connect", command_type=CommandType.CALL)
        async def connect(self, ctx, user: str, pw: str, **kwargs):
            self.identifier = user
            self.connection[user] = ctx

            ctx.write(
                protocol.ProtocolBuilder()
                    .set_method("connect")
                    .set_session(None)
                    .set_result({"is_success": True})
                    .build()
            )

        @command.command(method="sendFile_data", command_type=CommandType.CALL)
        async def send_file(self, ctx, header: dict, path: str, filename: str, data: bytes, **kwargs):
            raw_data = kwargs.get("raw")
            dst: str = header.get("to")

            sess = Server.DataListener.route(dst)
            sess.write(raw_data)

        @command.command(method="sendFile_data", command_type=CommandType.RESULT)
        async def send_file_result(self, ctx, header: dict, is_success: bool, **kwargs):
            raw_data = kwargs.get("raw")
            src: str = header.get("from")

            sess = Server.DataListener.route(src)
            sess.write(raw_data)
