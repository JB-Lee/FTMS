import socket
import threading
import unittest
from pprint import pprint

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
        "host": "167.179.91.13",
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
                + EOF
            )

            data = conn.recv(1024)
            data = bson.loads(data)

            print()
            print("Get UUID Test")
            pprint(data)

            self.assertIn("method", data)
            self.assertIn("result", data)
            self.assertIn("uuid", data["result"])

            globals()["ID"] = data.get("result").get("uuid")

    # def test_listdir(self):
    #     with Connection(HOST, PORT) as conn:
    #         conn.send(
    #             protocol.ProtocolBuilder()
    #             .set_method("listdir")
    #             .set_session(ID)
    #             .set_params({"header": {"from": "client-a", "to": "client-a", "requester": ID},
    #                          "path": "C://Temp"})
    #             .build()
    #             + EOF
    #         )
    #
    #         data = conn.recv(1024)
    #         data = bson.loads(data)
    #
    #         print()
    #         print("List Dir Test")
    #         pprint(data)
    #
    #         self.assertIn("method", data)

    # def test_send_file(self):
    #     with Connection(HOST, PORT) as conn:
    #         conn.send(
    #             protocol.ProtocolBuilder()
    #             .set_method("sendFile")
    #             .set_session(ID)
    #             .set_params({"header": {"from": "client-a", "to": "client-a", "requester": ID},
    #                          "src": {"path": "C:\\Temp", "file_name": "table.png"},
    #                          "dst": {"path": "C:\\Temp\\test", "file_name": "ubto.png"}})
    #             .build()
    #             + EOF
    #         )
    #
    #         data = conn.recv(1024)
    #         data = bson.loads(data)
    #
    #         print()
    #         print("Send File Test")
    #         pprint(data)
    #
    #         self.assertIn("method", data)

    def test_get_root(self):
        def sub(x):
            with Connection(HOST, PORT) as conn:
                conn.send(
                    protocol.ProtocolBuilder()
                    .set_method("get_root")
                    .set_session(ID + str(x))
                    .set_params({"header": {"from": "client-a", "requester": ID + str(x)}})
                    .build()
                    + EOF
                )

                data = conn.recv(1024)
                data = bson.loads(data)

                print()
                print("Get Root Test")
                pprint(data)

                self.assertIn("method", data)

        for x in range(20):
            threading.Thread(target=sub, args=(x,)).start()


def get_data(conn: socket.socket) -> dict:
    data = conn.recv(1024)
    data = data[:-len(EOF)]
    data = bson.loads(data)
    return data
