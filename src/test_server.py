import asyncio
import logging

import ftms_lib
import listeners

logging.basicConfig(level=logging.DEBUG)


def client_command_protocol_factory():
    p = ftms_lib.ContinuousProtocol()
    p.register_listener(listeners.Server.ClientCommandListener())
    return p


def app_command_protocol_factory():
    p = ftms_lib.SessionProtocol(ftms_lib.NullSessionHandler())
    p.register_listener(listeners.Server.AppCommandListener())
    return p


def data_protocol_factory():
    p = ftms_lib.ContinuousProtocol()
    p.register_listener(listeners.Server.DataListener())
    return p


async def main():
    loop = asyncio.get_running_loop()

    app_cmd_server = await loop.create_server(
        app_command_protocol_factory,
        "localhost",
        8088
    )

    client_cmd_server = await loop.create_server(
        client_command_protocol_factory,
        "localhost",
        8089
    )

    data_server = await loop.create_server(
        data_protocol_factory,
        "localhost",
        8082
    )

    async with app_cmd_server, client_cmd_server, data_server:
        await app_cmd_server.start_serving()
        await data_server.start_serving()
        await client_cmd_server.start_serving()

        await app_cmd_server.wait_closed()
        await data_server.wait_closed()
        await client_cmd_server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
