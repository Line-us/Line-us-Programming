# Getting Started with Line-us Programming
Line-us is a small internet connected robot drawing arm. It copies your movements in real time and draws with a real pen on paper. 

Line-us can be controlled using a simple API, either TCP Sockets or Websockets. The commands are a subset of GCode, loosely based on the [RepRap spec](http://reprap.org/wiki/G-code). The supported GCode set is described in the [GCode Specification Document](Documentation/GCodeSpec.md) but the primary command used for drawing is the G01 (interpolated move) command. 

Be sure to check out the [Line-us Drawing Area Diagram](Documentation/LineUsDrawingArea.pdf) which will tell you all you need to know about the co-ordinate system that Line-us uses and the shape of the drawing space.

The simplest way to get started is to try one of the examples below.
# Contents
#### Simple Example code to get you started with programming
- [Simple Python Example](#simple-python-example)
- [Simple Processing Example](#simple-processing-example)
- [Simple Node Example created by pandrr](#simple-node-example)
- [Simple Dart Example](#simple-dart-example)
- [Simple C Example created by Paul Haeberli](#simple-c-example)
- [Simple C# Unity Example created by soylentgraham](#simple-c-sharp-unity-example-poplineus)

#### Applications and other fun things to do with your Line-us
- [Line-us JS Kit created by funwithtriangles](#line-us-js-kit)
- [Java Generative app by @fiskdebug](#java-generative-app-by-fiskdebug)
- [SVG Plotter for Line-us by Michael Zöllner](#svg-plotter-by-michael-zöllner)

#### Libraries to make programming easy
- [Javascript Library by Beardicus](#javascript-library-by-beardicus)
- [PHP Library by fxmorin](#php-library-by-fxmorin)

#### Protocol details for people who want to know how it all works
- [Making a connection](#making-a-connection)
- [Sending GCode](#sending-gcode)
- [Responses from Line-us](#responses-from-line-us)
- [Timing](#timing)
- [Co-ordinate System](#co-ordinate-system)
- [CAUTION for firmware 1.0.1 and lower](#caution-for-firmware-101-and-lower)

## Simple Example code to get you started with programming
### Simple Python Example
There are two simple examples for python. [Source code](Python/HelloWorld.py#L1) for a very simple example using the TCP Sockets API can be downloaded from [here](../../raw/master/Python/HelloWorld.py). The example works with Python 2.7 and Python 3, but Python 3 is preferred. There is also [Source code](Python/HelloWorldWebsockets.py#L1) for a straightforward prot of the TCP example to use the websockets API that can be downloaded [here](../../raw/master/Python/HelloWorldWebsockets.py). For the sake of clarity the Websockets example tries to sidestep the use of asyncio by wrapping each of the async functions. 

### Simple Processing Example
[Source code](Processing/HelloWorld/HelloWorld.pde#L1) for a very simple example can be downloaded from [here](../../raw/master/Processing/HelloWorld/HelloWorld.pde). The example works with with Processing 3.3.7 (Java) - just copy and paste into your Processing window.

### Simple Node Example
Pandrr has ported our Python example to Node! - check out his GitHub [here](https://github.com/pandrr/line-us)

### Simple Dart Example
[Source code](Dart/line_us.dart) for a very simple example can be downloaded from [here](../../raw/master/Dart/line_us.dart). You'll need [Dart](https://www.dartlang.org/) installed.

### Simple C Example
[Source code](C/lineustest.c) for a simple example in C created by Paul Haberli can be downloaded from [here](../../raw/master/C/lineustest.c). The code complies on MACOS using gcc but should be fairly portable. A [Makefile](C/Makefile) is also included so if you have gcc in your path, just type 'make'

### Simple C Sharp Unity Example PopLineus
C# (wrapped in unity for now) implementation of the protocol for Line-us created by solentygraham, check out his GitHub [here](https://github.com/NewChromantics/PopLineus)

## Applications and other fun things to do with your Line-us
### Line-us Music
We've taught Line-us to play keyboards with some [simple Python3 code](Python/LineUsPlaysKeyboards.py#L1) that can be downloaded from [here](../../raw/master/Python/LineUsPlaysKeyboards.py). It's Python3 only so if you're on a Mac you'll need to install Python3 for it to work. We've put all of the keyboard code into a module, so you will need to istall that using `pip install lineusmusic`. When you install `lineusmusic` you'll also get the `lineus` module, but if you want to install that separately you can `pip install lineus`. As usual, we'd recommend using a virtual environment - my prefenece is [pipenv](https://thoughtbot.com/blog/how-to-manage-your-python-projects-with-pipenv) but there are a few options.

### Line-us JS Kit
Write commands in JavaScript and preview the drawing in your browser before sending to Line-us! Created by Alex Kempton, check out his Github [here](https://github.com/funwithtriangles/line-us-js-kit)

### Java Generative App By Fiskdebug
Very nice Java app available as [source](https://github.com/fiskurgit/Schroeder) or an [installable package for Mac](https://drive.google.com/open?id=1A-tzkwd0ce5_O0g8U3tDQ641fObSap1M) on @fiskfamilij's [GitHub](https://github.com/fiskurgit/Schroeder)

### SVG Plotter by Michael Zöllner
Great little app to plot your SVG files directly to Line-us. Available as [installers for Mac and Windows](https://github.com/ixd-hof/LineUs_SVG/releases) or [source](https://github.com/ixd-hof/LineUs_SVG) with instructions on [Michael's GitHub](https://github.com/ixd-hof/LineUs_SVG).

## Libraries to make programming easy
### Javascript Library by Beardicus
If you're thinking of writing some Javascript you should definitely check out this library as it will make your life *much* easier. It handles connection, queueing and all of the things you really don't want to do yourself. Works in the browser as well as with Node. Everything you need is at [Beardicus's GitHub](https://github.com/beardicus/line-us)

### PHP Library by fxmorin
A library created by fxmorin to allow you to use your Line-us with PHP. Available at [fxmorin's GitHub](https://github.com/fxmorin/line-us)

## Protocol details for people who want to know how it all works
### Introduction
As of firmware 3.0.0 Line-us offers a webscokets API as well as the original TCP Sockets API. All of the commands and responses are the same across both of the APIs, but there are a small number of commands that are not avaialble in the websockets API for security reasons (for example `M587` to set WiFi details). Details are in the [GCode Specification Document](Documentation/GCodeSpec.md).

### Making a Connection
The default name for Line-us is `line-us`, although it can be changed using the `M550` Gcode command or using the App. Line-us supports mDNS (Bonjour) so by default the hostname will be `line-us.local`. On a successful connection Line-us will respond with a `hello` message followed by `KEY:value` pairs for `VERSION` (firmware version number) `NAME` (the name of the Line-us) and `SERIAL` (the serial number of the Line-us). For example `hello VERSION:"3.2.0 Nov 17 2019 17:54:57" NAME:line-us SERIAL:123456`

##### TCP Sockets Connection
Line-us listens on TCP port 1337 and the connection to Line-us can be tested with a telnet client by using the command `telnet line-us.local 1337`. On connection you will receive the `hello` message, which (like all messages from Line-us) is terminated with `\r\n\0`. In firmware < 3.0.0 it was very important that the full `hello` message was read from the socket including the `\0` before any commands were sent. Firmware 3.0.0 or later has an improved TCP stack that means that this is no longer critical. It is still best to read the message though.

##### Websockets Connection
The websockets URL for your Line-us (assuming you're using the default name) is `ws://line-us.local`. Note that it is not a secure (`wss:`) websocket - unfortunately Line-us's tiny brain isn't quite up to running SSL. On connection you will receive the `hello` message and once you've received it you can start to send GCode. A simple way to experiment with the websockets API is to use [Firecamp](https://firecamp.app) - just connect and send one GCode per message.

### Sending Gcode
GCode commands are a command followed by a zero or more parameters separated by white space. Parameters are a single letter followed immediately by the value. The [GCode Specification Document](Documentation/GCodeSpec.md) has details of all of the available GCodes, but a simepl example would be `G01 X1000 Y0 Z1000` to move to point (1000, 0) with the pen up. Where necessary the values can be enclosed in double quotes `"` for example `M587 Smy-ssid P"password with spaces"` if you have spaces in your WiFi password. For TCP Sockets connections GCode commands _**must**_ be terminated by one of, or a combination of `\r`, `\n`, and `\0`. Websockets connections do not require any terminators in the messages. 

### Responses from Line-us
Each GCode response will result in a response message from Line-us, which will start with either `ok` indicating success, or `error` indicating an error and is followed by zero or more `KEY:value` pairs as described in the [GCode Specification Document](Documentation/GCodeSpec.md). For TCP Sockets the response message is terminated with `\r\n\0`. In firmware < 3.0.0 it was essential that the full response message was read from the socket including the `\0` before the next command was sent. This is no longer the case with firmware 3.0.0 or later although it is still advisable to read the messages. Fow websockets the respnse will be received in a text messsage.

### Timing
If a GCode command that moves the arm is sent to Line-us while the arm is still in motion the command will be accepted, but the response message will not be sent until the prior movement has completed. This means that the sender will remain in sync with the arm (at most there will be one outstanding command).

### Co-ordinate System
Line-us GCode commands use 'machine co-ordinates'. The origin point (0, 0) for the co-ordinate system is at the centre point of the servo shafts, and GCode commands use drawing units (100 drawing units is approximately 5mm). The home point for the arm is (1000, 1000). The z axis is the pen height; 0 is down and 1000 is up. The shape if the drawing area is not rectangular. See the [Line-us Drawing Area Diagram](Documentation/LineUsDrawingArea.pdf) for details. If a GCode for a movement outside of the drawing is sent Line-us will move to something approximating the closest it can get to that point while still remaining within the drawing area and lift the pen.

### CAUTION for firmware 1.0.1 and lower
It should not be possible to send a GCode that overstretches the arm, or causes it to hit the body of Line-us. However, in firmware 1.0.1 and lower there is an area where the pen screw can come into contact with the body. For y positions < 0 the x coordinate should be limited to x >= 700 by your software as firmware 1.0.1 and lower allow x >= 500 in this zone. This will has now been fixed so please update to the latest firmware.
