import asyncio
import logging
from abc import ABCMeta, abstractmethod
from typing import List, Optional

import bson

from . import command
from .session import SessionHandler, SessionStatus

logger = logging.getLogger(__name__)


class Context:
    __transport: asyncio.transports.Transport

    def __init__(self, transport):
        self.__transport = transport


class BaseProtocol(asyncio.Protocol, metaclass=ABCMeta):
    transport: asyncio.transports.Transport
    listeners: List[command.Listener]
    peer_name = None

    def __init__(self):
        loop = asyncio.get_running_loop()
        self.listeners = list()
        self.is_conn_lost = loop.create_future()
        self.is_listener_register = loop.create_future()

    def register_listener(self, listener: command.Listener):
        logger.debug(f"Register Listener: {listener.__class__.__name__} to {self.__class__.__name__}")
        self.is_listener_register.set_result(True)
        self.listeners.append(listener)

        if hasattr(self, "transport"):
            listener.on_register(self.transport)

    async def conn_lost(self):
        return await self.is_conn_lost

    def data_received(self, data: bytes) -> None:
        asyncio.create_task(self.async_data_received(data))

    def eof_received(self) -> Optional[bool]:
        return super().eof_received()

    def connection_made(self, transport: asyncio.transports.Transport) -> None:
        self.transport = transport
        self.peer_name = transport.get_extra_info("peername")

        for listener in self.listeners:
            listener.on_create(transport)

        logger.info(f"connection made: {self.peer_name}")

    def connection_lost(self, exc: Optional[Exception]) -> None:
        super().connection_lost(exc)

        for listener in self.listeners:
            listener.on_close(self.transport)

        self.is_conn_lost.set_result(True)
        logger.info(f"connection lost: {self.peer_name}")

    async def async_data_received(self, data: bytes):
        if len(self.listeners) <= 0:
            await self.is_listener_register

        for listener in self.listeners:
            listener.on_receive(self.transport, data)

        await self.command_processing(data)

    @abstractmethod
    async def command_processing(self, data: bytes) -> None:
        pass


class SessionProtocol(BaseProtocol):
    session_handler: SessionHandler
    method_whitelist: List[str]

    def __init__(self, session_handler: SessionHandler, method_whitelist: List[str] = None):
        super(SessionProtocol, self).__init__()

        if method_whitelist is None:
            method_whitelist = list()

        self.session_handler = session_handler
        self.method_whitelist = method_whitelist

    async def command_processing(self, data: bytes) -> None:
        raw_data = data
        data = bson.loads(data)
        method = data.get("method")
        session = data.get("session")
        params = data.get("params")
        result = data.get("result")

        logger.debug(f"method: {method} | session: {session} | params: {params} | result: {result}")

        session_status = self.session_handler.get_session_state(session)

        if (session_status == SessionStatus.INVALID) and (method not in self.method_whitelist):
            pass

        elif session_status == SessionStatus.EXPIRED:
            pass

        else:
            pass

        if params:
            await asyncio.gather(
                *[listener.invoke(self.transport, method, raw=raw_data, **params) for listener in self.listeners])
        else:
            await asyncio.gather(
                *[listener.invoke(self.transport, method, is_result=True, raw=raw_data, **result) for listener in
                  self.listeners])

        self.transport.write_eof()
        self.transport.close()


class ContinuousProtocol(BaseProtocol):
    async def command_processing(self, data: bytes) -> None:
        raw_data = data
        data = bson.loads(data)
        method = data.get("method")
        params = data.get("params")
        result = data.get("result")

        logger.debug(f"method: {method} | params: {params} | result: {result}")

        if params:
            await asyncio.gather(
                *[listener.invoke(self.transport, method, raw=raw_data, **params) for listener in self.listeners])
        elif result:
            await asyncio.gather(
                *[listener.invoke(self.transport, method, is_result=True, raw=raw_data, **result) for listener in
                  self.listeners])
