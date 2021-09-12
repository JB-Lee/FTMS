import socket
import uuid

import bson

from ftms_lib import protocol
from ftms_lib import utils

EOF = b"\r\n\t\n\r"

CONFIG_FILE = "app_cfg.json"
DEFAULT_CONFIG = {
    "ACCOUNT": {
        "id": "client-app",
        "password": "abc1234"
    },
    "SERVER": {
        "host": "0.0.0.0",
        "port": 8088
    }
}

config = utils.JsonConfiguration(CONFIG_FILE)
config.load()
config.set_default(DEFAULT_CONFIG)
config.save()

HOST = config.get("SERVER.host")
PORT = config.get("SERVER.port")


def handle_client(client):
    a = client.recv(1024)
    a = bson.loads(a)

    client.send(
        protocol.ProtocolBuilder()
        .set_method("getUuid")
        .set_session(None)
        .set_result({"uuid": str(uuid.uuid4())})
        .build()
        + EOF
    )

    client.close()


def main():
    sv = socket.create_server(("", PORT))

    while True:
        c, addr = sv.accept()
        handle_client(c)


if __name__ == '__main__':
    main()
