import asyncio
from typing import Optional

from ftms_lib import command, protocol
from ftms_lib.command import CommandType


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
    def route(cls, client_id: str) -> asyncio.transports.Transport:
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

    @command.command(method="default", command_type=CommandType.CALL)
    async def default_call(self, ctx, header: dict, *args, **kwargs):
        raw_data = kwargs.get("raw")
        dst: str = header.get("to")

        sess = DataListener.route(dst)
        if sess:
            sess.write(raw_data)
        else:
            await self.connection_not_found(ctx, kwargs.get("method"), kwargs.get("session"))

    @command.command(method="default", command_type=CommandType.RESULT)
    async def default_result(self, ctx, header: dict, *args, **kwargs):
        raw_data = kwargs.get("raw")
        src: str = header.get("from")

        sess = DataListener.route(src)
        if sess:
            sess.write(raw_data)
        else:
            await self.connection_not_found(ctx, kwargs.get("method"), kwargs.get("session"))
