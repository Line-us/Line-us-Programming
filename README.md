# Getting Started with Line-us Programming
Line-us is a small internet connected robot drawing arm. It copies your movements in real time and draws with a real pen on paper. 

Line-us can be controlled using a simple TCP sockets API. The commands are a subset of GCode, loosely based on the [RepRap spec](http://reprap.org/wiki/G-code). The supported GCode set is described in the [GCode Specification Document](../blob/master/Documentation/GCodeSpec1.0.0b.pdf) but the primary command used for drawing is the G01 (interpolated move) command.

# Contents
- [Making a connection](#making-a-connection)
- [Sending GCode](#sending-gcode)
- [Responses from Line-us](#responses-from-line-us)
- [Timing](#timing)

### Making a Connection
The default name for Line-us is `line-us`, although it can be changed using the `M550` Gcode command or using the App. Line-us supports mDNS (Bonjour) so by default the hostname will be `line-us.local` and it listens on port 1337. The connection to Line-us can be tested with a telnet client by using the command `telnet line-us.local 1337`. On a successful connection Line-us will respond with a `hello` message followed by `KEY:value` pairs for `VERSION` (firmware version number) `NAME` (the name of the Line-us) and `SERIAL` (the serial number of the Line-us). The `hello` message (like all messages from Line-us) is terminated with `\r\n\0`. It is **very important that the full `hello` message is read from the socket including the `\0` before any commands are sent**.

### Sending Gcode
GCode commands are a command followed by a zero or more parameters separated by white space. Paramters are a single letter followed immediately by the value. Where necessary the values can be enclosed in double quotes `"`. A GCode command can be terminated by one of, or a combination of `\r`, `\n`, and `\0`.

### Responses from Line-us
Each GCode response will result in a response message from Line-us, which will start with either `ok` indicating success, or `error` indicating an error and is followed by zero or more `KEY:value` pairs as described in the [GCode Specification Document](../blob/master/Documentation/GCodeSpec1.0.0b.pdf). The resonse message is terminated with `\r\n\0`, and it is **very important that the full response message is read from the socket including the `\0` before the next command is sent**.

### Timing
If a GCode command that moves the arm is sent to Line-us while the arm is still in motion the command will be accepted, but the response message will not be sent until the prior movement has completed. This means that the sender will reamin in sync with the arm (at most there will be one outstanding command). 
