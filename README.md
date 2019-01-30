# Getting Started with Line-us Programming
Line-us is a small internet connected robot drawing arm. It copies your movements in real time and draws with a real pen on paper. 

Line-us can be controlled using a simple TCP sockets API. The commands are a subset of GCode, loosely based on the [RepRap spec](http://reprap.org/wiki/G-code). The supported GCode set is described in the [GCode Specification Document](Documentation/GCodeSpec.pdf) but the primary command used for drawing is the G01 (interpolated move) command. 

Be sure to check out the [Line-us Drawing Area Diagram](Documentation/LineUsDrawingArea.pdf) which will tell you all you need to know about the co-ordinate system that Line-us uses and the shape of the drawing space.

The simplest way to get started is to try one of the examples below.
# Contents
#### Example code
- [Simple Python Example](#simple-python-example)
- [Simple Processing Example](#simple-processing-example)
- [Simple Node Example created by pandrr](#simple-node-example)
- [Line-us JS Kit created by funwithtriangles](#line-us-js-kit)
- [Simple C Example created by Paul Haeberli](#simple-c-example)
- [C# Unity Example created by soylentgraham](#c-sharp-unity-example-poplineus)
- [Java Generative app by @fiskdebug](#java-generative-app-by-fiskdebug)
- [Simple Dart Example](#simple-dart-example)
- [Simple SVG Plotter for Line-us by Michael Zöllner](#simple-svg-plotter-by-michael-zöllner)

#### Protocol details
- [Making a connection](#making-a-connection)
- [Sending GCode](#sending-gcode)
- [Responses from Line-us](#responses-from-line-us)
- [Timing](#timing)
- [Co-ordinate System](#co-ordinate-system)
- [CAUTION for firmware 1.0.1 and lower](#caution-for-firmware-101-and-lower)
---
### Simple Python Example
[Source code](Python/HelloWorld.py#L1) for a very simple example can be downloaded from [here](../../raw/master/Python/HelloWorld.py). The example works with Python 2.7 and Python 3, but Python 3 is preferred.

### Simple Processing Example
[Source code](Processing/HelloWorld/HelloWorld.pde#L1) for a very simple example can be downloaded from [here](../../raw/master/Processing/HelloWorld/HelloWorld.pde). The example works with with Processing 3.3.7 (Java) - just copy and paste into your Processing window.

### Simple Node Example
Pandrr has ported our Python example to Node! - check out his GitHub [here](https://github.com/pandrr/line-us)

### Line-us JS Kit
Write commands in JavaScript and preview the drawing in your browser before sending to Line-us! Created by Alex Kempton, check out his Github [here](https://github.com/funwithtriangles/line-us-js-kit)

### Simple C Example
[Source code](C/lineustest.c) for a simple example in C created by Paul Haberli can be downloaded from [here](../../raw/master/C/lineustest.c). The code complies on MACOS using gcc but should be fairly portable. A [Makefile](C/Makefile) is also included so if you have gcc in your path, just type 'make'

### C Sharp Unity Example PopLineus
C (wrapped in unity for now) implementation of the protocol for Line-us created by solentygraham, check out his GitHub [here](https://github.com/NewChromantics/PopLineus)

### Java Generative App By Fiskdebug
Very nice Java app available as [source](https://github.com/fiskurgit/Schroeder) or an [installable package for Mac](https://drive.google.com/open?id=1A-tzkwd0ce5_O0g8U3tDQ641fObSap1M) on @fiskfamilij's [GitHub](https://github.com/fiskurgit/Schroeder)

### Simple Dart Example
[Source code](Dart/line_us.dart) for a very simple example can be downloaded from [here](../../raw/master/Dart/line_us.dart). You'll need [Dart](https://www.dartlang.org/) installed.

### Simple SVG Plotter by Michael Zöllner
Great little app to plot your SVG files directly to Line-us. Available as [installers for Mac and Windows](https://github.com/ixd-hof/LineUs_SVG/releases) or [source](https://github.com/ixd-hof/LineUs_SVG) with instructions on [Michael's GitHub](https://github.com/ixd-hof/LineUs_SVG).

### Making a Connection
The default name for Line-us is `line-us`, although it can be changed using the `M550` Gcode command or using the App. Line-us supports mDNS (Bonjour) so by default the hostname will be `line-us.local` and it listens on port 1337. The connection to Line-us can be tested with a telnet client by using the command `telnet line-us.local 1337`. On a successful connection Line-us will respond with a `hello` message followed by `KEY:value` pairs for `VERSION` (firmware version number) `NAME` (the name of the Line-us) and `SERIAL` (the serial number of the Line-us). The `hello` message (like all messages from Line-us) is terminated with `\r\n\0`. It is **very important that the full `hello` message is read from the socket including the `\0` before any commands are sent**.

### Sending Gcode
GCode commands are a command followed by a zero or more parameters separated by white space. Parameters are a single letter followed immediately by the value. Where necessary the values can be enclosed in double quotes `"`. A GCode command can be terminated by one of, or a combination of `\r`, `\n`, and `\0`.

### Responses from Line-us
Each GCode response will result in a response message from Line-us, which will start with either `ok` indicating success, or `error` indicating an error and is followed by zero or more `KEY:value` pairs as described in the [GCode Specification Document](Documentation/GCodeSpec.pdf). The response message is terminated with `\r\n\0`, and it is **very important that the full response message is read from the socket including the `\0` before the next command is sent**.

### Timing
If a GCode command that moves the arm is sent to Line-us while the arm is still in motion the command will be accepted, but the response message will not be sent until the prior movement has completed. This means that the sender will remain in sync with the arm (at most there will be one outstanding command).

### Co-ordinate System
Line-us GCode commands use 'machine co-ordinates'. The origin point (0, 0) for the co-ordinate system is at the centre point of the servo shafts, and GCode commands use drawing units (100 drawing units is approximately 5mm). The home point for the arm is (1000, 1000). The z axis is the pen height; 0 is down and 1000 is up. The shape if the drawing area is not rectangular. See the [Line-us Drawing Area Diagram](Documentation/LineUsDrawingArea.pdf) for details. If a GCode for a movement outside of the drawing is sent Line-us will move to something approximating the closest it can get to that point while still remaining within the drawing area and lift the pen.

### CAUTION for firmware 1.0.1 and lower
It should not be possible to send a GCode that overstretches the arm, or causes it to hit the body of Line-us. However, in firmware 1.0.1 and lower there is an area where the pen screw can come into contact with the body. For y positions < 0 the x coordinate should be limited to x >= 700 by your software as firmware 1.0.1 and lower allow x >= 500 in this zone. This will has now been fixed so please update to the latest firmware.
