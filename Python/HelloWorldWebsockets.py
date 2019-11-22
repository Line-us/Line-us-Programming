import asyncio
import websockets
import time


class LineUs:
    """An example class to show how to use the Line-us WebSockets API"""

    def __init__(self, line_us_name):
        self.uri = f'ws://{line_us_name}'
        self.__line_us = None
        self.__hello_message = None
        self.__loop = asyncio.get_event_loop()

    def __del__(self):
        self.__loop.close()

    async def async_connect(self):
        self.__line_us = await websockets.connect(self.uri)
        self.__hello_message = await self.__line_us.recv()

    def connect(self):
        self.__loop.run_until_complete(self.async_connect())

    def get_hello_string(self):
        return self.__hello_message

    async def async_disconnect(self):
        await self.__line_us.close()

    def disconnect(self):
        self.__loop.run_until_complete(self.async_disconnect())

    async def async_send(self, message):
        await self.__line_us.send(message)
        reply = await self.__line_us.recv()
        return reply

    def send(self, message):
        reply = self.__loop.run_until_complete(self.async_send(message))
        return reply

    def g01(self, x, y, z):
        command = f'G01 X{x} Y{y} Z{z}'
        return self.send(command)


if __name__ == '__main__':
    my_line_us = LineUs('line-us-dev.local')
    my_line_us.connect()
    print(my_line_us.get_hello_string())
    time.sleep(1)

    my_line_us.g01(900, 300, 0)
    my_line_us.g01(900, -300, 0)
    my_line_us.g01(900, -300, 1000)

    my_line_us.g01(1200, 300, 0)
    my_line_us.g01(1200, -300, 0)
    my_line_us.g01(1200, -300, 1000)

    my_line_us.g01(900, 0, 0)
    my_line_us.g01(1200, 0, 0)
    my_line_us.g01(1200, 0, 1000)

    my_line_us.g01(1500, 150, 0)
    my_line_us.g01(1500, -300, 0)
    my_line_us.g01(1500, -300, 1000)

    my_line_us.g01(1500, 250, 0)
    my_line_us.g01(1500, 300, 0)
    my_line_us.g01(1500, 300, 1000)

    time.sleep(1)
    my_line_us.disconnect()
