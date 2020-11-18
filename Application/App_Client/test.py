import socket
import unittest

import bson

from ftms_lib import protocol
from ftms_lib import utils

CONFIG_FILE = "app_cfg.json"
DEFAULT_CONFIG = {
    "ACCOUNT": {
        "id": "client-app",
        "password": "abc1234"
    },
    "SERVER": {
        "host": "localhost",
        "port": 8088
    }
}

config = utils.JsonConfiguration(CONFIG_FILE)
config.load()
config.set_default(DEFAULT_CONFIG)
config.save()

ID = config.get("ACCOUNT.id")
PW = config.get("ACCOUNT.password")

HOST = config.get("SERVER.host")
PORT = config.get("SERVER.port")


class Connection:
    sock: socket.socket
    host: str
    port: int

    def __init__(self, host: str = "localhost", port: int = 8080):
        self.host = host
        self.port = port

    def __enter__(self):
        self.sock = socket.create_connection((self.host, self.port))
        return self.sock

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sock.close()


class MyTestCase(unittest.TestCase):
    def test_get_uuid(self):
        with Connection(HOST, PORT) as conn:
            conn.send(
                protocol.ProtocolBuilder()
                    .set_method("getUuid")
                    .build()
            )

            data = conn.recv(1024)
            data = bson.loads(data)

            print(data)

            self.assertIn("method", data)
            self.assertIn("result", data)
            self.assertIn("uuid", data["result"])

            globals()["ID"] = data.get("result").get("uuid")

    def test_send_file(self):
        with Connection(HOST, PORT) as conn:
            conn.send(
                protocol.ProtocolBuilder()
                    .set_method("sendFile")
                    .set_session(ID)
                    .set_params({"header": {"from": "client-a", "to": "client-a", "requester": ID},
                                 "src": {"path": "C:\\Temp", "file_name": "ubuntu.png"},
                                 "dst": {"path": "C:\\Temp\\test", "file_name": "ubto.png"}})
                    .build()
            )

            data = conn.recv(1024)
            data = bson.loads(data)

            print(data)

            self.assertIn("method", data)
