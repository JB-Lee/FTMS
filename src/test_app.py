import socket

import bson

from ftms_lib import protocol
from ftms_lib import utils

CONFIG_FILE = "app_cfg.json"
DEFAULT_CONFIG = {
    "id": "client-app",
    "password": "abc1234"
}

if __name__ == '__main__':
    config = utils.JsonConfiguration(CONFIG_FILE)
    config.load()
    config.set_default(DEFAULT_CONFIG)
    config.save()

    id = config.get("id")

    # c.send(
    #     protocol.ProtocolBuilder()
    #         .set_method("connect")
    #         .set_session(None)
    #         .set_params({"user": id,
    #                      "pw": "password1234"})
    #         .build()
    # )
    #
    # data = c.recv(1024)
    # data = bson.loads(data)
    # print(data)

    c = socket.create_connection(("localhost", 8088))

    c.send(
        protocol.ProtocolBuilder()
            .set_method("sendFile")
            .set_session(id)
            .set_params({"header": {"from": "client-a", "to": "client-a", "requester": id},
                         "src": {"path": "C:\\Temp", "file_name": "ubuntu.png"},
                         "dst": {"path": "C:\\Temp\\test", "file_name": "ubto.png"}})
            .build()
    )

    data = c.recv(1024)
    data = bson.loads(data)
    print(data)
    c.close()

    c = socket.create_connection(("localhost", 8088))

    c.send(
        protocol.ProtocolBuilder()
            .set_method("listdir")
            .set_session(id)
            .set_params({"header": {"from": "client-a", "requester": id},
                         "path": "C:\\Users"})
            .build()
    )

    data = c.recv(1024)
    data = bson.loads(data)
    print(data)
    c.close()
