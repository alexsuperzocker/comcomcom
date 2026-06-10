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

12 bits instruction adress + 4 bits op-code + 12 bits argument

Instructions are:

0000 'ADD' : adds value at argument adress onto accumulator
0001 'SUB' : subtracts value at argument adress from accumulator
0010 'MUL' : multiplies value at argument adress with accumulator
0011 'DIV' : divides value at accumulator with value at argument adress
0100 'LOD' : load value at argument adress into accumulator
0101 'STO' : store value from accumulator into argument adress
0110 'INP' : put argument into accumulator
0111 'JMP' : Jump (GoTo) argument instruction adress
1000 'JMZ' : Jump if accumulator value is equal to zero
1001 'JGZ' : Jump if accumulator value is greater than zero
1010 'FSH' : Flush values in special output registers to screen (still in discussion)
1011 'AWT' : Await 12 bit input from argument input device, block execution until input given. Input is put into accumulator.
1100 'HLT' : Halt (Stop) execution.
1101 'FNC' : Execute argument function (still in discussion)
1110 'ISF' : Is argument adress free aka not set via STO. Puts 1 into accumulator if adress is free, else 0.
1111 'DEL' : Frees (unsets) argument adress.


## Compiler

The compiler part of the project compiles source files to specific bytecode files.