# comcomcom

## The computer

The computer is a simulator of our Von-Neumann-style computer in minecraft.

The computer has...

...12 bits for adressing memory

...12 bits memory size (per cell)

=> 2^12 memory cells = 4096 memory cells

...12 bits for adressing instructions

=> 2^12 = 4096 instructions

The computer uses parity integer system (2^11 positive and negative integers), the first bit indicates the sign. This is mostly important for math and JGZ instructions. However, for almost all other applications, this does not matter and the numbers can be interpreted as unsigned integers (e.g. adresses).

An instruction consists of

12 bits instruction adress + 5 bits op-code + 12 bits argument

Instructions are:

00000 'ADD' : adds value at argument adress onto accumulator

00001 'SUB' : subtracts value at argument adress from accumulator

00010 'MUL' : multiplies value at argument adress with accumulator

00011 'DIV' : divides value at accumulator with value at argument adress

00100 'LOD' : load value at argument adress into accumulator

00101 'STO' : store value from accumulator into argument adress

00110 'INP' : put argument into accumulator

00111 'JMP' : Jump (GoTo) argument instruction adress

01000 'JMZ' : Jump if accumulator value is equal to zero

01001 'JGZ' : Jump if accumulator value is greater than zero

01010 'FSH' : Flush values in special output registers to screen (still in discussion)

01011 'AWT' : Await 12 bit input from argument input device, block execution until input given. Input is put into accumulator.

01100 'HLT' : Halt (Stop) execution.

01101 'FNC' : Execute argument function (still in discussion)

01110 'ISF' : Is argument adress free aka not set via STO. Puts 1 into accumulator if adress is free, else 0.

01111 'DEL' : Frees (unsets) argument adress.

10000 'ADI' : Adds argument to accumulator.

10001 'SBI' : Subtracts argument from accumulator.

10010 'MLI' : Multiplies argument onto accumulator.

10011 'DVI' : Divides accumulator by argument.

10100 'LDA' : Loads value at adress that is defined at argument adress into accumulator.

10101 'STA' : Stores value in accumulator to adress that is defined at argument adress.

10110 'GOA' : Jumps to adress that is defined at argument adress.

10111 'AND' : Performs bitwise 'and' over value at accumulator and value at argument adress. Result is written into accumulator.

11000 'ORE' : Performs bitwise 'or' over value at accumulator and value at argument adress. Result is written into accumulator.

11001 'XOR' : Performs bitwise 'xor' over value at accumulator and value at argument adress. Result is written into accumulator.

11010 'MOD' : Calculates abs(value at accumulator) mod abs(value at argument adress) and writes result to accumulator.

11011 'MDI' : Calculates abs(value at accumulator) mod abs(argument) and writes result to accumulator.

11100 'NOT' : Flips every bit of value in accumulator.

11111 'NOP' : No operation.


## Compiler

The compiler part of the project compiles source files to specific bytecode files. Takes in a .comc (comcode) file
and outputs a .ccc (compiled comcode) file.

### Comcode

Comcode is a assembly type coding language created by me, but heavily inspired by assembly. It is a machine oriented language, revolving around the (almost) 32 instructions (see above) we have set to implement in a minecraft computer. The minecraft computer is still in developement, but you can use the simulator (under /simulator) in this project to test your code. To simulate how instructions would be input on the minecraft computer, comcode needs to be compiled to (our custom) bytecode (.ccc files) using the compiler (under /compile)
before it can be run in the simulator.

When writing comcode, each line must have the following format:
```code
<instruction counter> <operator> <argument>
```

Where instruction counter and argument can be ommited. Missing instruction counter will internally be replaced with line number. Missing argument will be replaced with 0.
The instruction counter as well as the argument can be either a 12 bit string, a natural number between 0 and 4095,
a whole number between -2048 and 2047 or a hexadecimal number in the form #ZZZ.
The operator is either the 3 letter opcode or the 5 bit opcode (see above).

As of now, comments in either .comc or .ccc files are forbidden.

