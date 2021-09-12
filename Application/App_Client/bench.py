import concurrent.futures
import socket
import threading
import time

import bson
import numpy as np

from ftms_lib import protocol
from ftms_lib import utils

POOL = concurrent.futures.ThreadPoolExecutor()

CONNECTIONS = 100
REQUEST_PER_CONNECTION = 10

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

ID = config.get("ACCOUNT.id")
PW = config.get("ACCOUNT.password")

HOST = config.get("SERVER.host")
PORT = config.get("SERVER.port")

request_time = list()
response_time = list()
success = list()


class Connection:
    sock: socket.socket
    host: str
    port: int
    timeout: int

    def __init__(self, host: str = "localhost", port: int = 8080, timeout: int = 5):
        self.host = host
        self.port = port
        self.timeout = timeout

    def __enter__(self):
        self.sock = socket.create_connection((self.host, self.port), timeout=self.timeout)
        return self.sock

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sock.close()


def connection_test(loop: int):
    for x in range(loop):
        try:
            with Connection(HOST, PORT) as conn:
                conn.send(
                    protocol.ProtocolBuilder()
                    .set_method("getUuid")
                    .build()
                    + EOF
                )
                req_time = time.time()
                data = conn.recv(1024)
                res_time = time.time()
                data = bson.loads(data)
                success.append(True)

                request_time.append(req_time)
                response_time.append(res_time)

        except:
            success.append(False)


def main():
    print(f"커넥션 수: {CONNECTIONS}")
    print(f"커넥션 당 요청수: {REQUEST_PER_CONNECTION}")
    print(f"총 요청 수: {CONNECTIONS * REQUEST_PER_CONNECTION}")

    ts = [threading.Thread(target=connection_test, args=(REQUEST_PER_CONNECTION,)) for x in range(CONNECTIONS)]

    test_start = time.time()

    for t in ts:
        t.start()

    for t in ts:
        t.join()

    test_end = time.time()

    entire_time = test_end - test_start
    diff_time = np.array(response_time) - np.array(request_time)
    avg_diff_time = np.mean(diff_time)
    pw = CONNECTIONS * REQUEST_PER_CONNECTION / entire_time

    print(f"성공 요청 수: {len(response_time)}")
    print(f"총 소요 시간: {entire_time}")
    print(f"총 요청 소요 시간: {max(request_time) - min(request_time)}")
    print(f"총 응답 소요 시간: {max(response_time) - min(response_time)}")
    print(f"요청당 평균 응답 시간: {avg_diff_time}")
    print(f"요청당 최소 응답 시간: {min(diff_time)}")
    print(f"요청당 최대 응답 시간: {max(diff_time)}")
    print(f"초당 평균 처리량: {pw}")


if __name__ == '__main__':
    main()
