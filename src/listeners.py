import asyncio
import os

from ftms_lib import command, protocol
from ftms_lib.command import CommandType


class Client:
    class DataListener(command.Listener):
        command_ctx: asyncio.transports.Transport

        def __init__(self, command_ctx):
            super(Client.DataListener, self).__init__()
            self.command_ctx = command_ctx

        def on_create(self, ctx: asyncio.transports.Transport):
            pass

        def on_close(self, ctx: asyncio.transports.Transport):
            pass

        def on_register(self, ctx: asyncio.transports.Transport):
            ctx.write(
                protocol.ProtocolBuilder()
                    .set_method("connect")
                    .set_session("session-01")
                    .set_params({"user": "client-a",
                                 "pw": "password1234"})
                    .build()
            )

        def on_receive(self, ctx: asyncio.transports.Transport, data: bytes):
            pass

        @command.command(method="close", command_type=CommandType.CALL)
        async def close(self, ctx: asyncio.transports.Transport, **kwargs):
            pass

        @command.command(method="sendFile", command_type=CommandType.CALL)
        async def send_file(self, ctx: asyncio.transports.Transport, header, path, filename, data, **kwargs):
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
                        .set_method("sendFile")
                        .set_session("session-01")
                        .set_result({"header": header,
                                     "is_success": success})
                        .build()
                )

        @command.command(method="sendFile", command_type=CommandType.RESULT)
        async def send_file_result(self, ctx: asyncio.transports.Transport, header, is_success, **kwargs):
            raw_data = kwargs.get("raw")
            self.command_ctx.write(raw_data)

    class CommandListener(command.Listener):
        data_ctx: asyncio.transports.Transport

        def __init__(self, data_ctx):
            super(Client.CommandListener, self).__init__()
            self.data_ctx = data_ctx

        def on_create(self, ctx: asyncio.transports.Transport):
            pass

        def on_close(self, ctx: asyncio.transports.Transport):
            pass

        def on_receive(self, ctx: asyncio.transports.Transport, data: bytes):
            pass

        def on_register(self, ctx: asyncio.transports.Transport):
            ctx.write(
                protocol.ProtocolBuilder()
                    .set_method("connect")
                    .set_session("session-01")
                    .set_params({"user": "client-a",
                                 "pw": "password1234"})
                    .build()
            )

        @command.command(method="close")
        async def close(self, ctx: asyncio.transports.Transport, user, **kwargs):
            pass

        @command.command(method="listdir", command_type=CommandType.CALL)
        async def listdir(self, ctx: asyncio.transports.Transport, path, **kwargs):
            ctx.write(
                protocol.ProtocolBuilder()
                    .set_method("listdir")
                    .set_session("sess-01")
                    .set_result({"dirs": os.listdir(path)})
                    .build()
            )

            print(path)

        @command.command(method="sendFile", command_type=CommandType.CALL)
        async def send_file(self, ctx: asyncio.transports.Transport, src: dict, dst: dict, requester: str, **kwargs):
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
                        .set_method("sendFile")
                        .set_session("session-01")
                        .set_params({"header": {"from": src.get('id'),
                                                "to": dst.get("id"),
                                                "requester": requester},
                                     "path": dst_path,
                                     "filename": dst_file_name,
                                     "data": data})
                        .build()
                )

        @command.command(method="sendFile", command_type=CommandType.RESULT)
        async def send_file_result(self, ctx: asyncio.transports.Transport, header: dict, is_success: bool, **kwargs):
            raw_data = kwargs.get("raw")
            ctx.write(raw_data)


class Server:
    class ServerListener(command.Listener):
        connection: dict

        client_id: str
        client_pw: str

        def on_create(self, ctx: asyncio.transports.Transport):
            pass

        def on_close(self, ctx: asyncio.transports.Transport):
            if self.client_id:
                if self.client_id in self.connection:
                    self.connection.pop(self.client_id)

        def on_register(self, ctx: asyncio.transports.Transport):
            pass

        def on_receive(self, ctx: asyncio.transports.Transport, data: bytes):
            pass

        @classmethod
        def route(cls, client_id: str) -> asyncio.transports.Transport:
            return cls.connection.get(client_id)

    class CommandListener(ServerListener):
        connection: dict = dict()

        @command.command(method="connect", command_type=CommandType.CALL)
        async def connect(self, ctx, user, pw, **kwargs):
            self.client_id = user
            self.client_pw = pw
            self.connection[user] = ctx

            ctx.write(
                protocol.ProtocolBuilder()
                    .set_method("connect")
                    .set_session("session-01")
                    .set_result({"is_success": True})
                    .build()
            )

        @command.command(method="sendFile", command_type=CommandType.CALL)
        async def send_file(self, ctx, src: dict, dst: dict, requester: str, **kwargs):
            client_id = src.get("id")

            sess = self.route(client_id)
            sess.write(
                protocol.ProtocolBuilder()
                    .set_method("sendFile")
                    .set_session("session-01")
                    .set_params({"src": src,
                                 "dst": dst,
                                 "requester": requester})
                    .build()
            )

        @command.command(method="sendFile", command_type=CommandType.RESULT)
        async def send_file_result(self, ctx, header: dict, is_success: bool, **kwargs):
            self.logger.debug("sendFile")
            rid = header.get("requester")

            sess = self.route(rid)

            sess.write(kwargs.get("raw"))

        @command.command(method="close")
        async def close(self, ctx, hello, **kwargs):
            print(hello)

        @command.command(method="close", command_type=CommandType.RESULT)
        async def close_result(self, ctx, hello, **kwargs):
            print("hello")
            print(hello)

        @command.command(method="listdir", command_type=CommandType.RESULT)
        async def listdir_result(self, ctx, dirs, **kwargs):
            self.logger.debug("listdir")
            print(dirs)

    class DataListener(ServerListener):
        connection: dict = dict()

        @command.command(method="connect", command_type=CommandType.CALL)
        async def connect(self, ctx, user: str, pw: str, **kwargs):
            self.client_id = user
            self.client_pw = pw
            self.connection[user] = ctx

            ctx.write(
                protocol.ProtocolBuilder()
                    .set_method("connect")
                    .set_session("session-01")
                    .set_result({"is_success": True})
                    .build()
            )

        @command.command(method="sendFile", command_type=CommandType.CALL)
        async def send_file(self, ctx, header: dict, path: str, filename: str, data: bytes, **kwargs):
            dst: str = header.get("to")

            sess = self.route(dst)

            sess.write(
                protocol.ProtocolBuilder()
                    .set_method("sendFile")
                    .set_session("session-01")
                    .set_params({"header": header,
                                 "path": path,
                                 "filename": filename,
                                 "data": data})
                    .build()
            )

        @command.command(method="sendFile", command_type=CommandType.RESULT)
        async def send_file_result(self, ctx, header: dict, is_success: bool, **kwargs):
            self.logger.debug("sendFile")

            raw_data = kwargs.get("raw")

            src: str = header.get("from")

            sess = Server.CommandListener.route(src)
            sess.write(raw_data)
