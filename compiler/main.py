from file_man import pick_file, get_file_name, DEFAULT_COMPILED
from os.path import join

NUM_SIZE = 12
OP_SIZE = 5

OPS = {
    "ADD" : "00000",
    "SUB" : "00001",
    "MUL" : "00010",
    "DIV" : "00011",
    "LOD" : "00100",
    "STO" : "00101",
    "INP" : "00110",
    "JMP" : "00111",
    "JMZ" : "01000",
    "JGZ" : "01001",
    "FSH" : "01010",
    "AWT" : "01011",
    "HLT" : "01100",
    "FNC" : "01101",
    "ISF" : "01110",
    "DEL" : "01111",
    "ADI" : "10000",
    "SBI" : "10001",
    "MLI" : "10010",
    "DVI" : "10011",
    "LDA" : "10100",
    "STA" : "10101",
    "GOA" : "10110",
    "AND" : "10111",
    "ORE" : "11000",
    "XOR" : "11001",
    "MOD" : "11010",
    "MDI" : "11011",
    "NOT" : "11100",
    "NOP" : "11111"
}

HEX_SYM = [str(a) for a in range(10)]
HEX_SYM.extend(["A", "B", "C", "D", "E", "F"])
def is_valid_hex(string: str):
    if(not string.startswith("#") or len(string) != 4):
        return False
    
    for chr in string.upper()[1:]:
        if chr not in HEX_SYM:
            return False
        
    return True


def is_valid_bits(bits, length):
    if len(bits) != length:
        return False
    
    for bit in bits:
        if bit not in ["0", "1"]:
            return False
        
    return True

def translate_op(op : str):
    if(is_valid_bits(op, OP_SIZE)):
        return op

    global OPS

    return OPS.get(op.upper())

def translate_num(num):
    if(is_valid_bits(num, NUM_SIZE)):
        return num
    
    out = None
    try:    # decimal
        num = int(num)
        if(num > 2**NUM_SIZE - 1 or num < -1 * 2**(NUM_SIZE - 1)):
            raise f"Number {num} to large!"
        if(num >= 0):
            out = num
        else:
            out = 2**NUM_SIZE + num
    except(ValueError): # hexadecimal #ZZZ
        if(not is_valid_hex(num)):
            raise "Failed converting to bits! Invalid number format!"
        
        out = int(num.replace("#", "0x"), 16)
    
    return ('{0:0'+str(NUM_SIZE)+'b}').format(out)


class Instruction:
    seperator = " "

    def __init__(self, ic, op, arg):
        self.__ic = ic
        self.__op = op
        self.__arg = arg

    def translate_to_bits(self):
        bits = translate_num(self.__ic)
        bits += Instruction.seperator
        bits += translate_op(self.__op)
        bits += Instruction.seperator
        if(self.__arg is not None):
            bits += translate_num(self.__arg)
        else:
            bits += NUM_SIZE*"0"
        return bits
    
def read_instructions(file):
    lines = []
    with open(file, "r") as f:
        for line in f:
            lines.append(line)

    seperator = " "
    instructions = []
    i = 1
    for line in lines:
        try:
            split_1 = line.strip().split(seperator)
            ic, op, arg = None, None, None

            if(len(split_1) >= 3):
                ic = split_1[0]
                op = split_1[1]
                arg = split_1[2]
            
            elif(len(split_1) == 1):
                ic = ('{0:0'+str(NUM_SIZE)+'b}').format(i)
                op = split_1[0]

            else:
                if(split_1[0].upper() in OPS.keys()):
                    ic = ('{0:0'+str(NUM_SIZE)+'b}').format(i)
                    op = split_1[0]
                    arg = split_1[1]
                else:
                    ic = split_1[0]
                    op = split_1[1]
                
            
            instruction = Instruction(ic, op, arg)
            instructions.append(instruction)
        except:
            raise f"Error during reading of file! Could not convert line '{line}' to Instruction!"
        
        i += 1
    return instructions

def generate_binary(instructions):
    out = ""
    for instruction in instructions:
        out += instruction.translate_to_bits()
        out += "\n"
    return out

def write_binary(data, file_location):
    with open(file_location, "w+") as f:
        f.write(data)
    print(f"Successfully generated binary! Saved to {file_location}")

def main():
    path = pick_file()
    instructions = read_instructions(path)
    data = generate_binary(instructions)
    write_binary(data, join(DEFAULT_COMPILED, get_file_name(path) + ".ccc"))

if __name__ == "__main__":
    main()