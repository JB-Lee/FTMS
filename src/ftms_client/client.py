import asyncio
from typing import Optional, List

import bson

from . import protocol
from .listeners import DataListener, CommandListener

CLOSE = 1


class Client(asyncio.Protocol):
    transport: asyncio.transports.Transport
    listeners: List[protocol.Listener]

    def __init__(self):
        self.listeners = list()

    def register_listener(self, listener: protocol.Listener):
        self.listeners.append(listener)

    def data_received(self, data: bytes) -> None:
        super().data_received(data)

    def eof_received(self) -> Optional[bool]:
        return super().eof_received()

    def connection_made(self, transport: asyncio.transports.Transport) -> None:
        self.transport = transport

    def connection_lost(self, exc: Optional[Exception]) -> None:
        super().connection_lost(exc)

    async def command_processing(self, data: bytes) -> None:
        data = bson.loads(data)
        method = data.get("method")
        session = data.get("session")
        params = data.get("params")

        await asyncio.gather(*[listener.invoke(self.transport, method, **params) for listener in self.listeners])


def data_client_factory():
    client = Client()
    client.register_listener(
        DataListener()
    )
    return client


def command_client_factory():
    client = Client()
    client.register_listener(
        CommandListener()
    )
    return client


if __name__ == '__main__':
    pass
