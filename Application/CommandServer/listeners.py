import asyncio
import uuid
from typing import Optional

from ftms_lib import command, protocol, SessionContext
from ftms_lib.command import CommandType

LOCK = asyncio.Lock()


class ServerListener(command.Listener):
    connection: dict
    identifier: Optional[str]

    def on_create(self, ctx: asyncio.transports.Transport):
        pass

    def on_close(self, ctx: asyncio.transports.Transport):
        if hasattr(self, "identifier"):
            if self.identifier in self.connection:
                self.connection.pop(self.identifier)

    def on_register(self, ctx: asyncio.transports.Transport):
        pass

    def on_receive(self, ctx: asyncio.transports.Transport, data: bytes):
        pass

    async def on_command(self, ctx: asyncio.transports.Transport, *args, **kwargs):
        pass

    @classmethod
    async def route(cls, client_id: str) -> asyncio.transports.Transport:
        transport = cls.connection.get(client_id)
        return transport

    @classmethod
    async def connection_not_found(cls, ctx: asyncio.transports.Transport, method, session):
        ctx.write(
            protocol.ProtocolBuilder()
                .set_method(method)
                .set_session(session)
                .set_result({"is_success": False,
                             "error": "Connection cannot found"})
                .build()
        )


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

    @command.command(method="default", command_type=CommandType.RESULT)
    async def default_result(self, ctx, session, header, *args, **kwargs):
        raw_data = kwargs.get("raw")
        app_id = header.get("requester")

        with SessionContext(await AppCommandListener.route(app_id)) as sess:
            if sess:
                sess.write(raw_data)
            else:
                await self.connection_not_found(ctx, kwargs.get("method"), session)


class AppCommandListener(ServerListener):
    connection: dict = dict()
    counter: int = 0

    @classmethod
    def count(cls):
        cls.counter += 1
        if cls.counter > 10000:
            cls.counter = 0
        return cls.counter

    async def register_session(self, ctx, session: str):
        # session = f"{session}_{self.count()}"
        self.identifier = session
        self.connection[session] = ctx
        return session

    @command.command(method="default", command_type=CommandType.CALL)
    async def default_command(self, ctx, session, header, *args, **kwargs):
        await self.register_session(ctx, session)

        client_id = header.get("from")

        raw_data = kwargs.get("raw")

        sess = await ClientCommandListener.route(client_id)
        if sess:
            sess.write(raw_data)
        else:
            await self.connection_not_found(ctx, kwargs.get("method"), session)

    @command.command(method="getUuid", command_type=CommandType.CALL)
    async def get_uuid(self, ctx, session, **kwargs):

        with SessionContext(ctx) as sess:
            sess.write(
                protocol.ProtocolBuilder()
                    .set_method("getUuid")
                    .set_session(None)
                    .set_result({"uuid": str(uuid.uuid4())})
                    .build()
            )

    @command.command(method="ping", command_type=CommandType.CALL)
    async def ping(self, ctx, session, client, **kwargs):
        with SessionContext(ctx) as sess:
            sess.write(
                protocol.ProtocolBuilder()
                    .set_method("ping")
                    .set_session(None)
                    .set_result({"is_success": True if await ClientCommandListener.route(client) else False})
                    .build()
            )
