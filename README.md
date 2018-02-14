# Getting Started with Line-us Programming
Line-us is a small internet connected robot drawing arm. It copies your movements in real time and draws with a real pen on paper. 

Line-us can be controlled using a simple TCP sockets API. The commands are a subset of GCode, loosely based on the [RepRap spec](http://reprap.org/wiki/G-code). The supported GCode set is described in the [GCode Specification Document](Documentation/GCodeSpec.pdf) but the primary command used for drawing is the G01 (interpolated move) command.

# Contents
- [Making a connection](#making-a-connection)
- [Sending GCode](#sending-gcode)
- [Responses from Line-us](#responses-from-line-us)
- [Timing](#timing)
- [Co-ordinate System](#co-ordinate-system)
- [CAUTION for firmware 1.0.1 and lower](#caution-for-firmware-1.0.1-and-lower)
- [Simple Python Example](#simple-python-example)

### Making a Connection
The default name for Line-us is `line-us`, although it can be changed using the `M550` Gcode command or using the App. Line-us supports mDNS (Bonjour) so by default the hostname will be `line-us.local` and it listens on port 1337. The connection to Line-us can be tested with a telnet client by using the command `telnet line-us.local 1337`. On a successful connection Line-us will respond with a `hello` message followed by `KEY:value` pairs for `VERSION` (firmware version number) `NAME` (the name of the Line-us) and `SERIAL` (the serial number of the Line-us). The `hello` message (like all messages from Line-us) is terminated with `\r\n\0`. It is **very important that the full `hello` message is read from the socket including the `\0` before any commands are sent**.

### Sending Gcode
GCode commands are a command followed by a zero or more parameters separated by white space. Paramters are a single letter followed immediately by the value. Where necessary the values can be enclosed in double quotes `"`. A GCode command can be terminated by one of, or a combination of `\r`, `\n`, and `\0`.

### Responses from Line-us
Each GCode response will result in a response message from Line-us, which will start with either `ok` indicating success, or `error` indicating an error and is followed by zero or more `KEY:value` pairs as described in the [GCode Specification Document](Documentation/GCodeSpec.pdf). The resonse message is terminated with `\r\n\0`, and it is **very important that the full response message is read from the socket including the `\0` before the next command is sent**.

### Timing
If a GCode command that moves the arm is sent to Line-us while the arm is still in motion the command will be accepted, but the response message will not be sent until the prior movement has completed. This means that the sender will reamin in sync with the arm (at most there will be one outstanding command).

### Co-ordinate System
Line-us GCode commands use 'machine co-ordinates'. The origin point (0, 0) for the co-ordinate system is at the centre point of the servo shafts, and GCode commands use drawing units (100 drawing units is approximately 5mm). The home point for the arm is (1000, 1000). The z axis is the pen height; 0 is down and 1000 is up. The shape if the drawing area is not rectangular. See the [Line-us Drawing Area Diagram](Documentation/LineUsDrawingArea.pdf) for details. If a GCode for a movement outside of the drawing are is sent Line-us will move to something approximating the closest it can get to that point while still remaining within the drawing area. If the pen is on the down position (z < 500) the pen will lift (z = 1000).

### CAUTION for firmware 1.0.1 and lower
It should not be possible to send a GCode that overstretches the arm, or causes it to hit the body of Line-us. However, in firmware 1.0.1 and lower there is an area where the pen screw can come into contact with the body. For y positions < 0 the x coordinate should be limited to x >= 700 by your software as firmware 1.0.1 and lower allow x >= 500 in this zone. This will be fixed in firmware 1.0.2.

### Simple Python Example
Source code for a very simple example can be downloaded from [here](Python/HelloWorld.py). The example works with Python 2.7 and Python 3, but Python 3 is preferred.

