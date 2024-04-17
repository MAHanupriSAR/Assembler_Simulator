import math as m
import sys
to_open=sys.argv[1]
to_write=sys.argv[2]
# to_open="test5.txt"
# to_write = "simulator.txt"

line_list = []
main_list = []
r_type_opcode = ["0110011"]
i_type_opcode = ["0000011", "0010011", "1100111"]
s_type_opcode = ["0100011"]
b_type_opcode = ["1100011"]
u_type_opcode = ["0110111", "0010111"]
j_type_opcode = ["1101111"]

registers_list = ["x0", "x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9", "x10", "x11", "x12", "x13", "x14", "x15", "x16", "x17", "x18", "x19", "x20", "x21", "x22", "x23", "x24", "x25", "x26", "x27", "x28", "x29", "x30", "x31"]
memory_list = ["0x00010000", "0x00010004", "0x00010008", "0x0001000c", "0x00010010", "0x00010014", "0x00010018", "0x0001001c", "0x00010020", "0x00010024","0x00010028", "0x0001002c", "0x00010030", "0x00010034", "0x00010038","0x0001003c", "0x00010040", "0x00010044", "0x00010048", "0x0001004c","0x00010050", "0x00010054", "0x00010058", "0x0001005c", "0x00010060","0x00010064", "0x00010068", "0x0001006c", "0x00010070", "0x00010074","0x00010078", "0x0001007c"]

memory_values = {
    "0x00010000": 0,
    "0x00010004": 0,
    "0x00010008": 0,
    "0x0001000c": 0,
    "0x00010010": 0,
    "0x00010014": 0,
    "0x00010018": 0,
    "0x0001001c": 0,
    "0x00010020": 0,
    "0x00010024": 0,
    "0x00010028": 0,
    "0x0001002c": 0,
    "0x00010030": 0,
    "0x00010034": 0,
    "0x00010038": 0,
    "0x0001003c": 0,
    "0x00010040": 0,
    "0x00010044": 0,
    "0x00010048": 0,
    "0x0001004c": 0,
    "0x00010050": 0,
    "0x00010054": 0,
    "0x00010058": 0,
    "0x0001005c": 0,
    "0x00010060": 0,
    "0x00010064": 0,
    "0x00010068": 0,
    "0x0001006c": 0,
    "0x00010070": 0,
    "0x00010074": 0,
    "0x00010078": 0,
    "0x0001007c": 0
}

register_values = {
    "x0": 0,
    "x1": 0,
    "x2": 256,
    "x3": 0,
    "x4": 0,
    "x5": 0,
    "x6": 0,
    "x7": 0,
    "x8": 0,
    "x9": 0,
    "x10": 0,
    "x11": 0,
    "x12": 0,
    "x13": 0,
    "x14": 0,
    "x15": 0,
    "x16": 0,
    "x17": 0,
    "x18": 0,
    "x19": 0,
    "x20": 0,
    "x21": 0,
    "x22": 0,
    "x23": 0,
    "x24": 0,
    "x25": 0,
    "x26": 0,
    "x27": 0,
    "x28": 0,
    "x29": 0,
    "x30": 0,
    "x31": 0
}

register_decoder = {
    "00000": "x0",
    "00001": "x1",
    "00010": "x2",
    "00011": "x3",
    "00100": "x4",
    "00101": "x5",
    "00110": "x6",
    "00111": "x7",
    "01000": "x8",
    "01001": "x9",
    "01010": "x10",
    "01011": "x11",
    "01100": "x12",
    "01101": "x13",
    "01110": "x14",
    "01111": "x15",
    "10000": "x16",
    "10001": "x17",
    "10010": "x18",
    "10011": "x19",
    "10100": "x20",
    "10101": "x21",
    "10110": "x22",
    "10111": "x23",
    "11000": "x24",
    "11001": "x25",
    "11010": "x26",
    "11011": "x27",
    "11100": "x28",
    "11101": "x29",
    "11110": "x30",
    "11111": "x31"
}

binary_to_hex = {
    "0000": "0",
    "0001": "1",
    "0010": "2",
    "0011": "3",
    "0100": "4",
    "0101": "5",
    "0110": "6",
    "0111": "7",
    "1000": "8",
    "1001": "9",
    "1010": "A",
    "1011": "B",
    "1100": "C",
    "1101": "D",
    "1110": "E",
    "1111": "F"
}

def add_one_to_binary(binary_str):
    binary_list = [int(bit) for bit in binary_str]
    index = len(binary_list) - 1
    while index >= 0:
        if binary_list[index] == 0:
            binary_list[index] = 1
            break
        else:
            binary_list[index] = 0
            index -= 1
    if index < 0:
        binary_list.insert(0, 1)
    return ''.join(map(str, binary_list))
def binary_to_decimal(binary, signed = True):
    converted = 0
    if(signed == True):
        no_of_bits = len(binary)
        converted = converted + (int(binary[0]))*(-1**(int(binary[0])))*(2**(no_of_bits-1))
        for i in range(1,no_of_bits):
            converted = converted + (int(binary[i]))*(2**(no_of_bits-i-1))
    else:
        no_of_bits = len(binary)
        for i in range(0,no_of_bits):
            converted = converted + (int(binary[i]))*(2**(no_of_bits-i-1))
    return converted

def decimal_to_binary(imm):
    binary = ""
    if(imm>=0):
        while imm > 0:
            rem = str(imm % 2)
            binary = rem + binary
            imm //= 2
        binary = "0" + binary
    else:
        temp = abs(imm)
        while temp > 0:
            rem = str(temp % 2)
            binary = rem + binary
            temp //= 2
        binary = "0"+binary
        flipped_binary = ""
        for i in range(0, len(binary)):
            flipped_binary = flipped_binary + str(1-int(binary[i]))
        binary = flipped_binary
        binary = add_one_to_binary(binary)
    return binary

def binary_sign_extension(binary, max_bits, signed = True):
    no_of_bits = len(binary)
    bit_to_extend = max_bits - no_of_bits
    if(signed == True):
        if(binary[0] == "0"):
            binary = "0"*bit_to_extend + binary
        elif(binary[0] == "1"):
            binary = "1"*bit_to_extend + binary
    else:
        binary = "0"*bit_to_extend + binary
    return binary

def binary_to_hexadecimal(binary_string):
    decimal_number = int(binary_string, 2)  # Convert binary to decimal
    hex_number = hex(decimal_number)[2:]  # Convert decimal to hexadecimal
    hex_number = binary_sign_extension(str(hex_number), 8, False)
    return "0x"+hex_number

def r_type_instruction(line, line_number):
    line_number_to_return = line_number
    temp_list = []
    destination_register = line[20:25]
    source_register1 = line[12:17]
    source_register2 = line[7:12]
    func3 = line[17:20]
    func7 = line[0:7]
    destination_register = register_decoder[destination_register]
    source_register1 = register_decoder[source_register1]
    source_register2 = register_decoder[source_register2]
    if(func7 == "0000000" and func3 == "000"):
        source_register1 = register_values[source_register1]
        source_register2 = register_values[source_register2]
        add=source_register1+source_register2
        register_values[destination_register] = add

    elif(func7 == "0100000" and func3 == "000"):
        if(source_register1 == "x0"):
            source_register2 = register_values[source_register2]
            compliment= (m.pow(2,(m.floor(m.log2(source_register2))+1))-1)-source_register2 + 1
            register_values[destination_register] = compliment
        else:
            source_register1 = register_values[source_register1]
            source_register2 = register_values[source_register2]
            sub=source_register1-source_register2
            register_values[destination_register] = sub

    elif(func3 == "001"):
        source_register1 = register_values[source_register1]
        source_register2 = register_values[source_register2]
        leftshifter = binary_sign_extension(decimal_to_binary(source_register2), 32)[27:32]
        leftshifter = binary_to_decimal(leftshifter, False)
        left_shift=source_register1 << leftshifter 
        register_values[destination_register] = left_shift


    elif(func3 == "010"):
        source_register1 = register_values[source_register1]
        source_register2 = register_values[source_register2]
        if(source_register1<source_register2):
            register_values[destination_register] = 1

        
    elif(func3 == "011"):
        source_register1 = register_values[source_register1]
        source_register2 = register_values[source_register2]
        if(binary_to_decimal(decimal_to_binary(source_register1),False) < binary_to_decimal(decimal_to_binary(source_register2),False)):
            register_values[destination_register] = 1
    elif(func3 == "100"):
        source_register1 = register_values[source_register1]
        source_register2 = register_values[source_register2]
        xor=source_register1 ^ source_register2
        register_values[destination_register] = xor

        
    elif(func3 == "101"):
        source_register1 = register_values[source_register1]
        source_register2 = register_values[source_register2]
        rightshifter=binary_to_decimal((decimal_to_binary(source_register2))[27:32],False)
        right_shift=source_register1 >> rightshifter 
        register_values[destination_register] = right_shift
    elif(func3 == "110"):
        source_register1 = register_values[source_register1]
        source_register2 = register_values[source_register2]
        oor=source_register1|source_register2
        register_values[destination_register] = oor

        
    elif(func3 == "111"):
        source_register1 = register_values[source_register1]
        source_register2 = register_values[source_register2]
        aand=source_register1&source_register2
        register_values[destination_register] = aand
    
    line_number = (line_number+1)*4
    line_number = "0b" + binary_sign_extension(decimal_to_binary(line_number), 32)
    temp_list.append(line_number)
    for i in range(32):
        value_is = "0b" + binary_sign_extension(decimal_to_binary(register_values[registers_list[i]]), 32)
        temp_list.append(value_is)
    main_list.append(temp_list)

def i_type_instruction(line, line_number):
    line_number_to_return = line_number
    temp_list = []
    opcode = line[25:32]
    destination_register = line[20:25]
    func3 = line[17:20]
    source_register = line[12:17]
    immediate = line[0:12]
    destination_register = register_decoder[destination_register]
    source_register = register_decoder[source_register]
    if(opcode == "0000011" and func3 == "010"):
        source_register = register_values[source_register]
        immediate = binary_to_decimal(binary_sign_extension(immediate, 32))
        memory = binary_to_hexadecimal(decimal_to_binary(source_register + immediate))
        register_values[destination_register] = memory_values[memory]

    elif(opcode == "0010011" and func3 == "000"):
        immediate = binary_to_decimal(immediate)
        register_values[destination_register] = register_values[source_register] + immediate

    elif(opcode == "0010011" and func3 == "011"):
        unsinged_rs = binary_sign_extension(decimal_to_binary(register_values[source_register]), 32, False)
        unsigned_imm = binary_sign_extension(immediate, 32, False)
        unsinged_rs = binary_to_decimal(unsinged_rs, False)
        unsigned_imm = binary_to_decimal(unsigned_imm, False)
        if(unsinged_rs<unsigned_imm):
            register_values[destination_register] = 1

    elif(opcode == "1100111" and func3=="000"):
        register_values[destination_register] = (line_number*4)+4
        immediate = binary_to_decimal(binary_sign_extension(immediate, 32))
        program_counter = register_values[source_register] + immediate
        program_counter = binary_sign_extension(decimal_to_binary(program_counter), 32, False)
        program_counter = program_counter[0:31] + "0"
        to_append = "0b" + program_counter
        temp_list.append(to_append)
        program_counter = binary_to_decimal(program_counter, False)
        line_number_to_return = int(program_counter/4)
        line_number_to_return-=1
        for i in range(32):
            value_is = "0b" + binary_sign_extension(decimal_to_binary(register_values[registers_list[i]]), 32)
            temp_list.append(value_is)
        main_list.append(temp_list)
        return line_number_to_return

    line_number = (line_number+1)*4
    line_number = "0b" + binary_sign_extension(decimal_to_binary(line_number), 32)
    temp_list.append(line_number)
    for i in range(32):
        value_is = "0b" + binary_sign_extension(decimal_to_binary(register_values[registers_list[i]]), 32)
        temp_list.append(value_is)
    main_list.append(temp_list)
    return line_number_to_return

def s_type_instruction(line,line_number):
    line_number_to_return = line_number
    temp_list = []
    reg1_binary = line[12:17]
    reg2_binary = line[7:12]
    reg1_value = register_values[register_decoder[reg1_binary]]
    reg2_value = register_values[register_decoder[reg2_binary]]
    imm = ""
    imm = imm + line[0:7] + line[20:25]
    decimal_memory_address = reg1_value + binary_to_decimal(binary_sign_extension(imm, 32, signed=True), signed = True)
    binary_memory_address = decimal_to_binary(decimal_memory_address)
    hex_memory_address = binary_to_hexadecimal(binary_memory_address)
    memory_values[hex_memory_address] = reg2_value
    line_number = (line_number+1)*4
    line_number = "0b" + binary_sign_extension(decimal_to_binary(line_number), 32)
    temp_list.append(line_number)
    for i in range(32):
        value_is = "0b" + binary_sign_extension(decimal_to_binary(register_values[registers_list[i]]), 32)
        temp_list.append(value_is)
    main_list.append(temp_list)

def b_type_instruction(line, line_number):
    line_number_to_return = line_number
    temp_list = []
    pc = line_number*4
    imm_binary = ""
    imm_binary = imm_binary + line[0]
    imm_binary = imm_binary + line[24]
    imm_binary = imm_binary + line[1:7]
    imm_binary = imm_binary + line[20:24]
    imm_binary = imm_binary + "0"

    reg1_binary = line[12:17]
    reg2_binary = line[7:12]
    reg1_value = register_values[register_decoder[reg1_binary]]
    reg2_value = register_values[register_decoder[reg2_binary]]
    if(line[17:20] == "000"):
        if(reg1_value == reg2_value):
            pc = pc + binary_to_decimal(binary_sign_extension(imm_binary, 32, signed = True), signed=True)
    if(line[17:20] == "001"):
        if(reg1_value != reg2_value):
            pc = pc + binary_to_decimal(binary_sign_extension(imm_binary, 32, signed = True), signed=True)
    if(line[17:20] == "101"):
        if(reg1_value >= reg2_value):
            pc = pc + binary_to_decimal(binary_sign_extension(imm_binary, 32, signed = True), signed=True)
    if(line[17:20] == "111"):
        if(binary_to_decimal(decimal_to_binary(reg1_value),signed = False) >= binary_to_decimal(decimal_to_binary(reg2_value),signed = False)):
            pc = pc + binary_to_decimal(imm_binary, signed=True)
    if(line[17:20] == "100"):
        if(reg1_value < reg2_value):
            pc = pc + binary_to_decimal(binary_sign_extension(imm_binary, 32, signed = True), signed=True)
    if(line[17:20] == "110"):
        if(binary_to_decimal(decimal_to_binary(reg1_value),signed = False) < binary_to_decimal(decimal_to_binary(reg2_value),signed = False)):
            pc = pc + binary_to_decimal(binary_sign_extension(imm_binary, 32, signed = True), signed=True)

    if(int(pc/4)!=line_number):
        line_number = "0b" + binary_sign_extension(decimal_to_binary(pc), 32, False)
        temp_list.append(line_number)
    else:
        pc_value = (line_number+1)*4
        line_number = "0b" + binary_sign_extension(decimal_to_binary(pc_value), 32, False)
        temp_list.append(line_number)

    for i in range(32):
        value_is = "0b" + binary_sign_extension(decimal_to_binary(register_values[registers_list[i]]), 32)
        temp_list.append(value_is)
    main_list.append(temp_list)
    line_number = pc/4
    if(line_number_to_return==line_number):
        return line_number_to_return
    line_number-=1
    return int(line_number)

def u_type_instruction(line, line_number):
    temp_list = []
    Program_counter = line_number*4
    opcode = line[25:32]
    destination_register = line[20:25]
    immediate = line[0:20]
    if(opcode == "0010111"):
        register_values[register_decoder[destination_register]] = Program_counter + binary_to_decimal(binary_sign_extension((immediate + 12*"0"), 32, False))
    elif (opcode == "0110111"):
        register_values[register_decoder[destination_register]] = binary_to_decimal(binary_sign_extension((immediate + 12*"0"), 32, False))
    line_number = (line_number+1)*4
    line_number = "0b" + binary_sign_extension(decimal_to_binary(line_number), 32)
    temp_list.append(line_number)
    for i in range(32):
        value_is = "0b" + binary_sign_extension(decimal_to_binary(register_values[registers_list[i]]), 32)
        temp_list.append(value_is)
    main_list.append(temp_list)


def j_type_instruction(line, line_number):
    temp_list=[]
    program_counter = line_number*4
    destination_register = register_decoder[line[20:25]]
    imm = line[0:20]
    immediate = imm[1:11]
    immediate = imm[11] + immediate
    immediate = imm[12:20] + immediate
    immediate = imm[0] + immediate + "0"
    immediate = binary_to_decimal(binary_sign_extension(immediate, 32, False), False)
    register_values[destination_register] = program_counter + 4
    program_counter = program_counter + immediate
    temp_list.append("0b" + binary_sign_extension(decimal_to_binary(program_counter), 32, False))
    for i in range(32):
        value_is = "0b" + binary_sign_extension(decimal_to_binary(register_values[registers_list[i]]), 32)
        temp_list.append(value_is)
    line_number = int(program_counter/4)
    main_list.append(temp_list)
    line_number-=1
    return line_number


with open(to_open) as f:
    for line in f:    
        curr_line = line.strip()
        line_list.append(curr_line)


line_number = 0
while(line_number<len(line_list)):
    line = line_list[line_number]
    curr_line = line.strip()

    register_values["x0"] = 0
    if(len(main_list)>0):
        for inst in main_list:
            inst[1] = "0b00000000000000000000000000000000"
    if(line=="00000000000000000000000001100011"):
        if(len(main_list)>0):
            main_list.append(main_list[-1])
        break
    instruction_opcode = curr_line[25:32]   
    if(instruction_opcode in r_type_opcode):
        r_type_instruction(curr_line, line_number)   
            
    elif(instruction_opcode in i_type_opcode):
        line_number = int(i_type_instruction(curr_line, line_number))
        
    elif(instruction_opcode in s_type_opcode):
        s_type_instruction(curr_line, line_number)

    elif(instruction_opcode in b_type_opcode):
        line_number = int(b_type_instruction(curr_line, line_number))

    elif(instruction_opcode in u_type_opcode):
        u_type_instruction(curr_line, line_number)

    elif(instruction_opcode in j_type_opcode):
        line_number = int(j_type_instruction(curr_line, line_number))

    line_number+=1
    # with open(to_write, "a") as f:
    #     for num in register_values.values():
    #         f.write(str(num))
    #         f.write(" ")
    #     f.write("\n")

with open(to_write, "a") as f:
    for line in main_list:
        for instruction in line:
            f.write(str(instruction))
            f.write(" ")
        f.write("\n")

with open(to_write, "a") as f:
    for address in memory_list:
        f.write(address)
        f.write(":")
        f.write("0b"+ binary_sign_extension(decimal_to_binary(memory_values[address]), 32))
        f.write("\n")
