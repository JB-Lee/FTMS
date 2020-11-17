import asyncio
import logging

import ftms_lib
import listeners

logging.basicConfig(level=logging.DEBUG)


async def main():
    loop = asyncio.get_running_loop()

    # cmd_t, cmd_proto
    cmd_t, cmd_proto = await loop.create_connection(
        lambda: ftms_lib.ContinuousProtocol(),
        "localhost",
        8081
    )
    cmd_proto.pause_writing()

    # data_t, data_proto
    data_t, data_proto = await loop.create_connection(
        lambda: ftms_lib.ContinuousProtocol(),
        "localhost",
        8082
    )
    data_proto.pause_writing()

    if isinstance(cmd_proto, ftms_lib.ContinuousProtocol):
        cmd_proto.register_listener(listeners.Client.CommandListener(data_t))

    if isinstance(data_proto, ftms_lib.ContinuousProtocol):
        data_proto.register_listener(listeners.Client.DataListener(cmd_t))

    try:
        if isinstance(cmd_proto, ftms_lib.ContinuousProtocol) and isinstance(data_proto, ftms_lib.ContinuousProtocol):
            cmd_proto.resume_writing()
            data_proto.resume_writing()
            await cmd_proto.conn_lost()
            await data_proto.conn_lost()
    finally:
        cmd_t.close()
        data_t.close()


if __name__ == '__main__':
    asyncio.run(main())
