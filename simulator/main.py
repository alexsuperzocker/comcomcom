
NUM_SIZE = 12
OP_SIZE = 4

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
        return int(f"0b{bitstring}")
    else:
        return -1 * 2**NUM_SIZE + int(f"0b{bitstring}")

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
    def __init__(self):
        self.accu : str = zeroes()
        self.ic : str = zeroes()
        self.ram = {}
        self.instructions = {}
        self.__running = True

    def __increment_ic(self):
        self.ic = bitwise_arithmatic(self.ic, zeroes(), lambda a, _: a + 1)

    def halt(self):
        self.__running = False

    def add(self, arg):
        if(not is_valid_bits(arg, NUM_SIZE)):
            raise "Invalid value!"
        
        self.accu = bitwise_arithmatic(self.accu, arg, lambda a, b: a + b)

        self.__increment_ic()

    def sub(self, arg):
        if(not is_valid_bits(arg, NUM_SIZE)):
            raise "Invalid value!"
        
        self.accu = bitwise_arithmatic(self.accu, arg, lambda a, b: a - b)

        self.__increment_ic()

    def mul(self, arg):
        if(not is_valid_bits(arg, NUM_SIZE)):
            raise "Invalid value!"
        
        self.accu = bitwise_arithmatic(self.accu, arg, lambda a, b: a * b)

        self.__increment_ic()

    def div(self, arg):
        if(not is_valid_bits(arg, NUM_SIZE)):
            raise "Invalid value!"
        
        self.accu = bitwise_arithmatic(self.accu, arg, lambda a, b: int(a / b))

        self.__increment_ic()

    def load(self, adress):
        if(not is_valid_bits(adress, NUM_SIZE)):
            raise "Invalid memory adress!"

        if(adress in self.ram.keys()):
            self.accu = zeroes()
        else:
            self.accu = self.ram.get(adress)

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

    def flush(self):
        print("FLUSH!")

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

