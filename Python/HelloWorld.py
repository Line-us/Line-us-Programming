import socket
import time


class LineUs:
    """An example class to show how to use the Line-us API"""

    def __init__(self, line_us_name):
        self.__line_us = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__line_us.connect((line_us_name, 1337))
        self.__connected = True
        self.__hello_message = self.__read_response()

    def get_hello_string(self):
        if self.__connected:
            return self.__hello_message.decode()
        else:
            return 'Not connected'

    def disconnect(self):
        """Close the connection to the Line-us"""
        self.__line_us.close()
        self.__connected = False

    def g01(self, x, y, z):
        """Send a G01 (interpolated move, and wait for the response before returning"""
        cmd = b'G01 X'
        cmd += str(x).encode()
        cmd += b' Y'
        cmd += str(y).encode()
        cmd += b' Z'
        cmd += str(z).encode()
        self.__send_command(cmd)
        self.__read_response()

    def __read_response(self):
        """Read form the socket one byte at a time until we get a null"""
        line = b''
        while True:
            char = self.__line_us.recv(1)
            if char != b'\x00':
                line += char
            elif char == b'\x00':
                break
        return line

    def __send_command(self, command):
        """Send the command to Line-us"""
        command += b'\x00'
        self.__line_us.send(command)


#
#   Very simple example of how to use the Line-us API. The most important thing to
#   remember is to read the response after sending a command. The TCP buffer on
#   Line-us is small and it does not cope well with having to buffer more than
#   one message.
#
#   Good Luck!
#


my_line_us = LineUs('line-us.local')
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

