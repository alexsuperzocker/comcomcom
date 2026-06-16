import simul_i_o
from file_man import pick_file
from time import sleep

NUM_SIZE = 12
OP_SIZE = 5
DELAY = 0
DEBUG = False

def is_valid_bits(bits, length):
    if len(bits) != length:
        return False
    
    for bit in bits:
        if bit not in ["0", "1"]:
            return False
        
    return True

def zeroes():
    return NUM_SIZE*"0"

def convert_to_int(bitstring):
    if(bitstring[0] == "0"):
        return int(f"0b{bitstring}", 2)
    else:
        return -1 * 2**NUM_SIZE + int(f"0b{bitstring}", 2)

def bitwise_arithmatic(v1, v2, func):
    int_v1 = convert_to_int(v1)
    int_v2 = convert_to_int(v2)

    res = func(int_v1, int_v2)

    if(res < 0):
        res *= -1
        res = res % 2**NUM_SIZE
        res = -1 * 2**NUM_SIZE + res
    
    return (('{0:0'+str(NUM_SIZE)+'b}').format(res))[-NUM_SIZE:]

class Computer:
    def __init__(self, instructions):
        self.accu : str = zeroes()
        self.ic : str = ("0"*(NUM_SIZE-1))+"1"
        self.ram = {}
        self.instructions = instructions
        self.__running = True

        self.func_map = {
            "00000" : self.add,
            "00001" : self.sub,
            "00010" : self.mul,
            "00011" : self.div,
            "00100" : self.load,
            "00101" : self.store,
            "00110" : self._input,
            "00111" : self.jump,
            "01000" : self.jump_zero,
            "01001" : self.jump_greater_zero,
            "01010" : self.flush,
            "01011" : self._await,
            "01100" : self.halt,
            "01101" : self.func,
            "01110" : self.isfree,
            "01111" : self.delete,
            "10000" : self.add_imm,
            "10001" : self.sub_imm,
            "10010" : self.mul_imm,
            "10011" : self.div_imm,
            "10100" : self.load_adr,
            "10101" : self.store_adr,
            "10110" : self.go_adr,
            "10111" : self._and,
            "11000" : self._or,
            "11001" : self._xor,
            "11010" : self._mod,
            "11011" : self._mod_imm,
            "11100" : self._not,
            "11111" : self.noop
        }

    def __increment_ic(self):
        self.ic = bitwise_arithmatic(self.ic, zeroes(), lambda a, _: a + 1)

    def halt(self, _=zeroes()):
        self.__running = False

    def add(self, arg):
        if(not is_valid_bits(arg, NUM_SIZE)):
            raise "Invalid value!"
        
        self.accu = bitwise_arithmatic(self.accu, self.ram.get(arg, zeroes()), lambda a, b: a + b)

        self.__increment_ic()

    def sub(self, arg):
        if(not is_valid_bits(arg, NUM_SIZE)):
            raise "Invalid value!"
        
        self.accu = bitwise_arithmatic(self.accu, self.ram.get(arg, zeroes()), lambda a, b: a - b)

        self.__increment_ic()

    def mul(self, arg):
        if(not is_valid_bits(arg, NUM_SIZE)):
            raise "Invalid value!"
        
        self.accu = bitwise_arithmatic(self.accu, self.ram.get(arg, zeroes()), lambda a, b: a * b)

        self.__increment_ic()

    def div(self, arg):
        if(not is_valid_bits(arg, NUM_SIZE)):
            raise "Invalid value!"
        
        self.accu = bitwise_arithmatic(self.accu, self.ram.get(arg, zeroes()), lambda a, b: int(a / b))

        self.__increment_ic()

    def load(self, adress):
        if(not is_valid_bits(adress, NUM_SIZE)):
            raise "Invalid memory adress!"

        self.accu = self.ram.get(adress, zeroes())

        self.__increment_ic()

    def store(self, adress):
        if(not is_valid_bits(adress, NUM_SIZE)):
            raise "Invalid memory adress!"
        
        if(adress in self.ram.keys()):
            self.ram[adress] = self.accu
        else:
            self.ram.update({adress : self.accu})

        self.__increment_ic()

    def _input(self, value):
        if(not is_valid_bits(value, NUM_SIZE)):
            raise "Invalid value!"
        
        self.accu = value

        self.__increment_ic()

    def jump(self, ic):
        if(not is_valid_bits(ic, NUM_SIZE)):
            raise "Invalid value!"
        
        if(ic in self.instructions.keys()):
            self.ic = ic
        else:
            self.halt()

    def jump_zero(self, ic):
        if(self.accu == zeroes()):
            self.jump(ic)
        else:
            self.__increment_ic()

    def jump_greater_zero(self, ic):
        if(self.accu[0] != "1" and self.accu != zeroes()):
            self.jump(ic)
        else:
            self.__increment_ic()

    def flush(self, _=zeroes()):
        if(DEBUG):
            print("FLUSH!")

        simul_i_o.flush(self.get_out_registers())

        self.__increment_ic()

    def func(self, arg):
        print("Not implemented!")

        self.__increment_ic()

    def isfree(self, adress):
        if(not is_valid_bits(adress, NUM_SIZE)):
            raise "Invalid memory adress!"
        
        if(adress in self.ram.keys()):
            self.accu = zeroes()
        else:
            self.accu = ("0"*(NUM_SIZE - 1))+"1"

        self.__increment_ic()
    
    def delete(self, adress):
        if(not is_valid_bits(adress, NUM_SIZE)):
            raise "Invalid memory adress!"
        
        if(adress in self.ram.keys()):
            self.ram.pop(adress)

        self.__increment_ic()

    def _await(self, adress):
        if(not is_valid_bits(adress, NUM_SIZE)):
            raise "Invalid memory adress!"
        
        self.accu = simul_i_o.usr_input(adress)

        self.__increment_ic()

    def add_imm(self, arg):
        if(not is_valid_bits(arg, NUM_SIZE)):
            raise "Invalid value!"

        self.accu = bitwise_arithmatic(self.accu, arg, lambda a, b: a + b)
        self.__increment_ic()

    def sub_imm(self, arg):
        if(not is_valid_bits(arg, NUM_SIZE)):
            raise "Invalid value!"
        
        self.accu = bitwise_arithmatic(self.accu, arg, lambda a, b: a - b)
        self.__increment_ic()

    def mul_imm(self, arg):
        if(not is_valid_bits(arg, NUM_SIZE)):
            raise "Invalid value!"
        
        self.accu = bitwise_arithmatic(self.accu, arg, lambda a, b: a * b)
        self.__increment_ic()

    def div_imm(self, arg):
        if(not is_valid_bits(arg, NUM_SIZE)):
            raise "Invalid value!"
        
        self.accu = bitwise_arithmatic(self.accu, arg, lambda a, b: a / b)
        self.__increment_ic()

    def go_adr(self, adress):
        if(not is_valid_bits(adress, NUM_SIZE)):
            raise "Invalid memory adress!"
        
        ic = self.ram.get(adress, zeroes())

        self.jump(ic)
        
    def store_adr(self, adress):
        if(not is_valid_bits(adress, NUM_SIZE)):
            raise "Invalid memory adress!"
        
        adr = self.ram.get(adress, zeroes())

        self.store(adr)
        
    def load_adr(self, adress):
        if(not is_valid_bits(adress, NUM_SIZE)):
            raise "Invalid memory adress!"
        
        adr = self.ram.get(adress, zeroes())

        self.load(adr)
        
    def _and(self, adress):
        if(not is_valid_bits(adress, NUM_SIZE)):
            raise "Invalid memory adress!"
        
        arg = self.ram.get(adress, zeroes())
        result = ""

        for i in range(NUM_SIZE):
            if(self.accu[i] == "1" and arg[i] == "1"):
                result += "1"
            else:
                result += "0"

        self.accu = result
        
        self.__increment_ic()
        
    def _or(self, adress):
        if(not is_valid_bits(adress, NUM_SIZE)):
            raise "Invalid memory adress!"
        
        arg = self.ram.get(adress, zeroes())
        result = ""

        for i in range(NUM_SIZE):
            if(self.accu[i] == "1" or arg[i] == "1"):
                result += "1"
            else:
                result += "0"

        self.accu = result
        
        self.__increment_ic()
        
    def _not(self, _):
        self.accu = bitwise_arithmatic(self.accu, zeroes(), lambda a, _: (a * -1) - 1)
        self.__increment_ic()

    def _xor(self, adress):
        if(not is_valid_bits(adress, NUM_SIZE)):
            raise "Invalid memory adress!"
        
        arg = self.ram.get(adress, zeroes())
        result = ""

        for i in range(NUM_SIZE):
            if((self.accu[i] == "1" or arg[i] == "1") and not (self.accu[i] == "1" and arg[i] == "1")):
                result += "1"
            else:
                result += "0"

        self.accu = result

        self.__increment_ic()

    def _mod(self, adress):
        if(not is_valid_bits(adress, NUM_SIZE)):
            raise "Invalid memory adress!"
        
        self.accu = bitwise_arithmatic(self.accu, self.ram.get(adress, zeroes()), lambda a, b: abs(a) % abs(b))
        self.__increment_ic()

    def _mod_imm(self, arg):
        if(not is_valid_bits(arg, NUM_SIZE)):
            raise "Invalid value!"
        
        self.accu = bitwise_arithmatic(self.accu, arg, lambda a, b: abs(a) % abs(b))
        self.__increment_ic()

    def noop(self, _=zeroes()):
        self.__increment_ic()

    def get_out_registers(self):
        registers = []
        for i in range(12):
            adress = ('{0:0'+str(NUM_SIZE)+'b}').format(i)
            registers.append(self.ram.get(adress, zeroes()))

        return registers
    
    def is_running(self):
        return self.__running
    
    def tick(self):
        instruction = self.instructions.get(self.ic)
        #print(instruction)
        op, arg = instruction

        funct = self.func_map.get(op)

        if(DEBUG):
            print(f"{self.ic = }")
            print(f"{self.accu = }")
            print(f"{op = }")
            print(f"{arg = }")

        funct(arg)

        if(DEBUG):
            print(f"Executed operation {op} {arg}")
    
def load_computer(file):
    lines = []
    with open(file, "r") as f:
        for line in f:
            lines.append(line)

    instructions = {}
    seperator = " "
    for line in lines:
        split_1 = line.strip().split(seperator)
        ic = split_1[0]
        op = split_1[1]
        arg = split_1[2]
        instructions.update({ic : (op, arg)})

    comp = Computer(instructions)
    return comp

def main():
    path = pick_file()
    comp = load_computer(path)
    while(comp.is_running()):
        comp.tick()
        sleep(DELAY)
    print("Computer terminated!")

if __name__ == "__main__":
    main()