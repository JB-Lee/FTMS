import asyncio

__all__ = (
    "Protocol",
    "protocol"
)


class Protocol:

    def __init__(self, func, **kwargs):
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("콜백은 반드시 코루틴이여야 합니다.")

        self.method = kwargs.get("method") or func.__name__
        self.enabled = kwargs.get("enabled", True)
        self.callback = func

    async def __call__(self, *args, **kwargs):
        return await self.callback(*args, **kwargs)


def protocol(method=None, **kwargs):
    def wrapper(func):
        return Protocol(func, method=method, **kwargs)

    return wrapper
