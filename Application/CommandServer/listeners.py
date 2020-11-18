import asyncio
import uuid
from typing import Optional

from ftms_lib import command, protocol, SessionContext
from ftms_lib.command import CommandType


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

        with SessionContext(AppCommandListener.route(app_id)) as sess:
            sess.write(raw_data)

    @command.command(method="listdir", command_type=CommandType.RESULT)
    async def listdir_result(self, ctx, header: dict, dirs: list, **kwargs):
        raw_data = kwargs.get("raw")
        app_id = header.get("requester")

        with SessionContext(AppCommandListener.route(app_id)) as sess:
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

        sess = ClientCommandListener.route(client_id)
        sess.write(raw_data)

    @command.command(method="listdir", command_type=CommandType.CALL)
    async def listdir(self, ctx, session, header: dict, path: str, **kwargs):
        self.register_session(ctx, session)

        raw_data = kwargs.get("raw")
        client_id = header.get("from")

        sess = ClientCommandListener.route(client_id)
        sess.write(raw_data)

    @command.command(method="getUuid", command_type=CommandType.CALL)
    async def listdir(self, ctx, session, **kwargs):
        self.register_session(ctx, session)

        with SessionContext(ctx) as sess:
            sess.write(
                protocol.ProtocolBuilder()
                    .set_method("getUuid")
                    .set_session(None)
                    .set_result({"uuid": str(uuid.uuid4())})
                    .build()
            )
