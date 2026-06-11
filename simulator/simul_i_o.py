from main import is_valid_bits, NUM_SIZE

HEX_SYM = [str(a) for a in range(10)]
HEX_SYM.extend(["A", "B", "C", "D", "E", "F"])
def is_valid_hex(string: str):
    if(not string.startswith("#") or len(string) != 4):
        return False
    
    for chr in string.upper()[1:]:
        if chr not in HEX_SYM:
            return False
        
    return True

def translate_num(num):
    if(is_valid_bits(num, NUM_SIZE)):
        return num
    
    out = None
    try:    # decimal
        num = int(num)
        if(num > 2**NUM_SIZE - 1 or num < -1 * 2**(NUM_SIZE - 1)):
            return None
        if(num >= 0):
            out = num
        else:
            out = 2**NUM_SIZE + num
    except(ValueError): # hexadecimal #ZZZ
        if(not is_valid_hex(num)):
            return None
        
        out = int(num.replace("#", "0x"), 16)
    
    return ('{0:0'+str(NUM_SIZE)+'b}').format(out)

def flush(out_registers):
    for register in out_registers:
        print("|", end="")
        for bit in register:
            if(bit == "1"):
                print("#", end="|")
            else:
                print("_", end="|")
        print()
    print()

def usr_input(input_device_adress):
    usr_inp = None
    while(usr_inp is None):
        usr_inp = translate_num(input(f"Programm is expecting input from input device adress {input_device_adress}: \n"))
    return usr_inp