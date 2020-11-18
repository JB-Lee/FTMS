import asyncio
import logging

import listeners

import ftms_lib
from ftms_lib import utils

logging.basicConfig(level=logging.DEBUG)

CONFIG_FILE = "command_server_cfg.json"
DEFAULT_CONFIG = {
    "app_server": {
        "host": "localhost",
        "port": 8088
    },

    "client_server": {
        "host": "localhost",
        "port": 8089
    }
}

config = utils.JsonConfiguration(CONFIG_FILE)
config.load()
config.set_default(DEFAULT_CONFIG)
config.save()

APP_SERVER_HOST = config.get("app_server.host")
APP_SERVER_PORT = config.get("app_server.port")

CLIENT_SERVER_HOST = config.get("client_server.host")
CLIENT_SERVER_PORT = config.get("client_server.port")


def client_command_protocol_factory():
    protocol = ftms_lib.ContinuousProtocol()
    protocol.register_listener(listeners.ClientCommandListener())
    return protocol


def app_command_protocol_factory():
    protocol = ftms_lib.SessionProtocol(ftms_lib.NullSessionHandler())
    protocol.register_listener(listeners.AppCommandListener())
    return protocol


async def main():
    loop = asyncio.get_running_loop()

    app_cmd_server = await loop.create_server(
        app_command_protocol_factory,
        APP_SERVER_HOST,
        APP_SERVER_PORT,
        reuse_address=True
    )

    client_cmd_server = await loop.create_server(
        client_command_protocol_factory,
        CLIENT_SERVER_HOST,
        CLIENT_SERVER_PORT,
        reuse_address=True
    )

    async with app_cmd_server, client_cmd_server:
        await app_cmd_server.start_serving()
        await client_cmd_server.start_serving()

        await app_cmd_server.wait_closed()
        await client_cmd_server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
