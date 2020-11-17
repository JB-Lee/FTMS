import socket

import bson

from ftms_lib import protocol

if __name__ == '__main__':
    c = socket.create_connection(("localhost", 8081))

    id = "client-app"

    c.send(
        protocol.ProtocolBuilder()
            .set_method("connect")
            .set_session("session-01")
            .set_params({"user": id,
                         "pw": "password1234"})
            .build()
    )

    data = c.recv(1024)
    data = bson.loads(data)
    print(data)

    c.send(
        protocol.ProtocolBuilder()
            .set_method("sendFile")
            .set_session("session-01")
            .set_params({"src": {"id": "client-a", "path": "C:\\Temp", "file_name": "ubuntu.png"},
                         "dst": {"id": "client-a", "path": "C:\\Temp\\test", "file_name": "ubto.png"},
                         "requester": id})
            .build()
    )

    data = c.recv(1024)
    data = bson.loads(data)
    print(data)
    c.close()
