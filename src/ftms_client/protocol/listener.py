import asyncio
from abc import abstractmethod, ABCMeta
from typing import Any

from .core import Protocol

__all__ = (
    "Listener",
)


class Listener(metaclass=ABCMeta):

    def __new__(cls, *args, **kwargs):
        __commands = dict()

        for elem, value in cls.__dict__.items():
            if isinstance(value, Protocol):
                __commands[value.method] = value

        new_cls = super().__new__(cls)
        new_cls.__commands = __commands
        return new_cls

    async def invoke(self, ctx: asyncio.transports.Transport, method: Any, *args, **kwargs):
        func = self.__commands.get(method, False)
        if func:
            return await func(self, ctx=ctx, *args, **kwargs)
        else:
            return None

    @abstractmethod
    def on_create(self):
        pass

    @abstractmethod
    def on_close(self):
        pass
