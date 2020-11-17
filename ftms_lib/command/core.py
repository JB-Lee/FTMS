import asyncio
from enum import Enum

__all__ = (
    "Command",
    "command",
    "CommandType"
)


class CommandType(Enum):
    CALL = 0
    RESULT = 1


class Command:

    def __init__(self, func, command_type: CommandType, **kwargs):
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("콜백은 반드시 코루틴이여야 합니다.")

        self.method = kwargs.get("method") or func.__name__
        self.enabled = kwargs.get("enabled", True)
        self.command_type = command_type
        self.callback = func

    async def __call__(self, *args, **kwargs):
        return await self.callback(*args, **kwargs)


def command(command_type: CommandType = CommandType.CALL, method=None, **kwargs):
    def wrapper(func):
        return Command(func, command_type, method=method, **kwargs)

    return wrapper
