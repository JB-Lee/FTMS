import asyncio
import logging

import listeners

import ftms_lib
from ftms_lib import utils

logging.basicConfig(level=logging.DEBUG)

CONFIG_FILE = "data_server_cfg.json"
DEFAULT_CONFIG = {
    "data_server": {
        "host": "localhost",
        "port": 8082
    }
}

config = utils.JsonConfiguration(CONFIG_FILE)
config.load()
config.set_default(DEFAULT_CONFIG)
config.save()

SERVER_HOST = config.get("data_server.host")
SERVER_PORT = config.get("data_server.port")


def data_protocol_factory():
    p = ftms_lib.ContinuousProtocol()
    p.register_listener(listeners.DataListener())
    return p


async def main():
    loop = asyncio.get_running_loop()

    data_server = await loop.create_server(
        data_protocol_factory,
        SERVER_HOST,
        SERVER_PORT,
        reuse_address=True
    )

    async with data_server:
        await data_server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
