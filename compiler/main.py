
NUM_SIZE = 12
OP_SIZE = 4

OPS = {
    "ADD" : "0000",
    "SUB" : "0001",
    "MUL" : "0010",
    "DIV" : "0011",
    "LOD" : "0100",
    "STO" : "0101",
    "INP" : "0110",
    "JMP" : "0111",
    "JMZ" : "1000",
    "JGZ" : "1001",
    "FSH" : "1010",
    "AWT" : "1011",
    "HLT" : "1100",
    "FNC" : "1101",
    "ISF" : "1110",
    "DEL" : "1111"
}

HEX_SYM = [str(a) for a in range(10)].extend(["A", "B", "C", "D", "E", "F"])
def is_valid_hex(string: str):
    if(not string.startswith("#") or len(string) != 4):
        return False
    
    for chr in string[1:]:
        if chr.upper() not in HEX_SYM:
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
        if(num >= 0):
            out = num
        else:
            out = 2**NUM_SIZE + num
    except: # hexadecimal #ZZZ
        if(not is_valid_hex(num)):
            raise "Failed converting to bits! Invalid number format!"
        
        out = int(num.replace("#", "0x"), 16)
    
    return ('{0:0'+NUM_SIZE+'b}').format(out)


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
        bits += translate_num(self.__arg)
        return bits

def main():
    ...

if __name__ == "__main__":
    main()