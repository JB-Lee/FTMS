import asyncio
import logging
from abc import abstractmethod, ABCMeta
from typing import Any

from .core import Command, CommandType

__all__ = (
    "Listener",
)

logger = logging.getLogger(__name__)


class Listener(metaclass=ABCMeta):

    def __new__(cls, *args, **kwargs):
        __commands = dict()
        __commands_result = dict()

        for elem, value in cls.__dict__.items():
            if isinstance(value, Command):
                if value.command_type == CommandType.RESULT:
                    __commands_result[value.method] = value
                else:
                    __commands[value.method] = value

        new_cls = super().__new__(cls)
        new_cls.__commands = __commands
        new_cls.__commands_result = __commands_result
        new_cls.logger = logging.getLogger(f"{__name__}.{new_cls.__class__.__qualname__}")
        return new_cls

    async def invoke(self, ctx: asyncio.transports.Transport, method: Any, is_result: bool = False, *args, **kwargs):
        func = self.__commands_result.get(method, False) if is_result else self.__commands.get(method, False)
        if func:
            return await func(self, ctx=ctx, *args, **kwargs)
        else:
            logger.warning(f"Method {method}.{'RESULT' if is_result else 'CALL'} is not defined.")
            return None

    @abstractmethod
    def on_create(self, ctx: asyncio.transports.Transport):
        pass

    @abstractmethod
    def on_close(self, ctx: asyncio.transports.Transport):
        pass

    @abstractmethod
    def on_register(self, ctx: asyncio.transports.Transport):
        pass

    @abstractmethod
    def on_receive(self, ctx: asyncio.transports.Transport, data: bytes):
        pass
