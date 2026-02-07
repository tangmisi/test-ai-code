```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const CalculatorApp());
}

class CalculatorApp extends StatelessWidget {
  const CalculatorApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Local AI Calculator',
      theme: ThemeData(primarySwatch: Colors.blue, useMaterial3: true),
      home: const CalculatorScreen(),
    );
  }
}

class CalculatorScreen extends StatefulWidget {
  const CalculatorScreen({super.key});

  @override
  State<CalculatorScreen> createState() => _CalculatorScreenState();
}

class _CalculatorScreenState extends State<CalculatorScreen> {
  String _output = "0";
  String _currentInput = "";
  double _num1 = 0;
  double _num2 = 0;
  String _operand = "";

  void _buttonPressed(String buttonText) {
    setState(() {
      if (buttonText == "C") {
        _output = "0";
        _currentInput = "";
        _num1 = 0;
        _num2 = 0;
        _operand = "";
      } else if (buttonText == "+" || buttonText == "-" || buttonText == "×" || buttonText == "÷") {
        _num1 = double.parse(_output);
        _operand = buttonText;
        _currentInput = "";
      } else if (buttonText == "=") {
        _num2 = double.parse(_output);
        if (_operand == "+") _output = (_num1 + _num2).toString();
        if (_operand == "-") _output = (_num1 - _num2).toString();
        if (_operand == "×") _output = (_num1 * _num2).toString();
        if (_operand == "÷") _output = (_num1 / _num2).toString();
        _num1 = 0;
        _num2 = 0;
        _operand = "";
        _currentInput = _output;
      } else {
        _currentInput += buttonText;
        _output = _currentInput;
      }
    });
  }

  Widget _buildButton(String text, {Color color = Colors.grey}) {
    return Expanded(
      child: Padding(
        padding: const EdgeInsets.all(4.0),
        child: ElevatedButton(
          style: ElevatedButton.styleFrom(
            padding: const EdgeInsets.symmetric(vertical: 20),
            backgroundColor: color,
            foregroundColor: Colors.white,
          ),
          onPressed: () => _buttonPressed(text),
          child: Text(text, style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("AI Generated Calculator")),
      body: Column(
        children: [
          Container(
            alignment: Alignment.centerRight,
            padding: const EdgeInsets.symmetric(vertical: 48, horizontal: 12),
            child: Text(_output, style: const TextStyle(fontSize: 60, fontWeight: FontWeight.bold)),
          ),
          const Spacer(),
          Column(
            children: [
              Row(children: [_buildButton("7"), _buildButton("8"), _buildButton("9"), _buildButton("÷", color: Colors.orange)]),
              Row(children: [_buildButton("4"), _buildButton("5"), _buildButton("6"), _buildButton("×", color: Colors.orange)]),
              Row(children: [_buildButton("1"), _buildButton("2"), _buildButton("3"), _buildButton("-", color: Colors.orange)]),
              Row(
                children: [
                  ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 20),
                      backgroundColor: Colors.green,
                      foregroundColor: Colors.white,
                    ),
                    onPressed: () => _buttonPressed("C"),
                    child: Text('C', style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                  ),
                  _buildButton("0"),
                  ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 20),
                      backgroundColor: Colors.green,
                      foregroundColor: Colors.white,
                    ),
                    onPressed: () => _buttonPressed("="),
                    child: Text('=', style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                  ),
                  _buildButton("+", color: Colors.orange)
                ],
              ),
            ],
          )
        ],
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerDocked,
      floatingActionButton: FloatingActionButton(
        onPressed: () {},
        tooltip: 'Add',
        child: Icon(Icons.add),
      ),
    );
  }
}
```