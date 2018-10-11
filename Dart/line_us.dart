import 'dart:convert';
import 'dart:io';

main() async {
  var commands = [
    'G01 X900 Y300 Z0',
    'G01 X900 Y-300 Z0',
    'G01 X900 Y-300 Z1000',
    'G01 X1200 Y300 Z0',
    'G01 X1200 Y-300 Z0',
    'G01 X1200 Y-300 Z1000',
    'G01 X900 Y0 Z0',
    'G01 X1200 Y0 Z0',
    'G01 X1200 Y0 Z1000',
    'G01 X1500 Y150 Z0',
    'G01 X1500 Y-300 Z0',
    'G01 X1500 Y-300 Z1000',
    'G01 X1500 Y250 Z0',
    'G01 X1500 Y300 Z0',
    'G01 X1500 Y300 Z1000',
  ];

  await LineUs(commands).draw();
}

class LineUs {
  final List<String> commandQueue;

  LineUs(this.commandQueue);

  Socket _socket;

  draw() async {
    _socket = await Socket.connect("line-us.local", 1337);

    _socket.transform(utf8.decoder).listen((data) {
      print(data);

      if (commandQueue.isNotEmpty) {
        final command = commandQueue.removeAt(0);
        _sendCommand(command);
      } else {
        _socket.destroy();
      }
    }, onError: (error) {
      print(error);
      _socket.destroy();
    });
  }

  _sendCommand(String command) async {
    _socket.write(command + "\x00\n");
  }
}
