import asyncio
import logging

import ftms_lib
import listeners

logging.basicConfig(level=logging.DEBUG)


def command_protocol_factory():
    p = ftms_lib.ContinuousProtocol()
    p.register_listener(listeners.Server.CommandListener())
    return p


def data_protocol_factory():
    p = ftms_lib.ContinuousProtocol()
    p.register_listener(listeners.Server.DataListener())
    return p


async def main():
    loop = asyncio.get_running_loop()

    cmd_server = await loop.create_server(
        command_protocol_factory,
        "localhost",
        8081
    )

    data_server = await loop.create_server(
        data_protocol_factory,
        "localhost",
        8082
    )

    async with cmd_server, data_server:
        await cmd_server.start_serving()
        await data_server.start_serving()

        await cmd_server.wait_closed()
        await data_server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
