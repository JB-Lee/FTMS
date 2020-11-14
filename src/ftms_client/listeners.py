import asyncio

from . import protocol


class DataListener(protocol.Listener):
    @protocol.protocol(method="close")
    async def close(self, ctx: asyncio.transports.Transport):
        pass

    def on_create(self):
        pass

    def on_close(self):
        pass


class CommandListener(protocol.Listener):
    @protocol.protocol(method="close")
    async def close(self, ctx: asyncio.transports.Transport):
        pass

    def on_create(self):
        pass

    def on_close(self):
        pass
