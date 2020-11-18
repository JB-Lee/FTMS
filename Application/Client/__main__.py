import asyncio
import logging

import listeners

import ftms_lib
from ftms_lib import utils

logging.basicConfig(level=logging.DEBUG)

CONFIG_FILE = "client_cfg.json"
DEFAULT_CONFIG = {
    "account": {
        "id": "client-a",
        "password": "abc1234"
    },

    "data_server": {
        "host": "0.0.0.0",
        "port": 8082
    },

    "command_server": {
        "host": "0.0.0.0",
        "port": 8089
    }

}

config = utils.JsonConfiguration(CONFIG_FILE)
config.load()
config.set_default(DEFAULT_CONFIG)
config.save()

ID = config.get("account.id")
PW = config.get("account.password")

DATA_SERVER_HOST = config.get("data_server.host")
DATA_SERVER_PORT = config.get("data_server.port")

COMMAND_SERVER_HOST = config.get("command_server.host")
COMMAND_SERVER_PORT = config.get("command_server.port")

print(DATA_SERVER_PORT)
print(DATA_SERVER_HOST)

print(COMMAND_SERVER_PORT)
print(COMMAND_SERVER_HOST)


async def main():
    loop = asyncio.get_running_loop()

    # cmd_t, cmd_proto
    cmd_t, cmd_proto = await loop.create_connection(
        lambda: ftms_lib.ContinuousProtocol(),
        COMMAND_SERVER_HOST,
        COMMAND_SERVER_PORT
    )

    # data_t, data_proto
    data_t, data_proto = await loop.create_connection(
        lambda: ftms_lib.ContinuousProtocol(),
        DATA_SERVER_HOST,
        DATA_SERVER_PORT
    )

    if isinstance(cmd_proto, ftms_lib.ContinuousProtocol):
        cmd_proto.register_listener(listeners.CommandListener(data_t, ID, PW))

    if isinstance(data_proto, ftms_lib.ContinuousProtocol):
        data_proto.register_listener(listeners.DataListener(cmd_t, ID, PW))

    try:
        if isinstance(cmd_proto, ftms_lib.ContinuousProtocol) and isinstance(data_proto, ftms_lib.ContinuousProtocol):
            await cmd_proto.conn_lost()
            await data_proto.conn_lost()

    finally:
        cmd_t.close()
        data_t.close()


if __name__ == '__main__':
    asyncio.run(main())
