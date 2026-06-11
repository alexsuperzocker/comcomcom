from main import is_valid_bits, NUM_SIZE

def flush(out_registers):
    for register in out_registers:
        for bit in register:
            if(bit == "1"):
                print("#", end="")
            else:
                print("_", end="")
        print()
    print()

def usr_input(input_device_adress):
    usr_inp = ""
    while(not is_valid_bits(usr_inp, NUM_SIZE)):
        usr_inp = input(f"Programm is expecting input from input device adress {input_device_adress}: \n")
    return usr_inp