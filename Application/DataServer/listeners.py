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

        sess = DataListener.route(dst)
        sess.write(raw_data)

    @command.command(method="sendFile_data", command_type=CommandType.RESULT)
    async def send_file_result(self, ctx, header: dict, is_success: bool, **kwargs):
        raw_data = kwargs.get("raw")
        src: str = header.get("from")

        sess = DataListener.route(src)
        sess.write(raw_data)
