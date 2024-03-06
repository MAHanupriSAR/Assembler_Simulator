line_number = 0
flag_of_error = False

def imm_binary_calc(imm):
    if imm < (-2048) or imm > 2047:
        return False
    else:
        binary = ""
        if(imm>=0):
            while imm > 0:
                rem = str(imm % 2)
                binary = rem + binary
                imm //= 2
        else:
            imm = abs(int(pow(2,12)-1) - abs(imm) + 1)
            while imm > 0:
                rem = str(imm % 2)
                binary = rem + binary
                imm //= 2

        if len(binary) < 12:
            if imm < 0:
                binary = "1" * (12 - len(binary)) + binary
            else:
                binary = "0" * (12 - len(binary)) + binary

        return binary

def reg_binary_calc(register_name):
    if register_name in registers:
        return list(registers[register_name].values())[0]
    else:
        return False
    
def binary_representation(num, i):
    num = abs(num)
    b=""
    for i in range(i):
        r = num%2
        b+= str(r)
        num//=2
    return b[::-1]

def binary_rep_compliment(num, bits):
    num = abs(num)
    maximum = int(pow(2, bits)-1)
    num = maximum - num
    num+=1
    return binary_representation(num, bits)

def convertible(num, bits):
    try:
        num = int(num)
        min = int((pow(2, bits-1))*(-1))
        max = int((pow(2, bits-1))-1)
        if int(num)>=min and int(num)<=max:
            return True
        else:
            return False
    except ValueError:
        return False


r_type = ["add", "sub", "sll", "slt", "sltu", "xor", "srl", "or", "and"]
i_type = ["lw", "addi", "sltiu", "jalr"]
s_type = ["sw"]
b_type = ["beq", "bne", "blt", "bge", "bge", "bltu", "bgeu"]
u_type = ["lui", "auipc"]
j_type = ["jal"]

r_function3={"add":"000","sub":"000","slt":"010","sltu":"011","xor":"100","sll":"001","srl":"101","or":"110","and":"111"}
i_opcode = {"lw":"0000011", "addi":"0010011", "sltiu":"0010011", "jalr":"1100111"}
i_funct3 = {"lw":"010", "addi":"000", "sltiu":"011", "jalr":"000"}

registers = {
    "zero": {"x0": "00000"},
    "ra": {"x1": "00001"},
    "sp": {"x2": "00010"},
    "gp": {"x3": "00011"},
    "tp": {"x4": "00100"},
    "t0": {"x5": "00101"},
    "t1": {"x6": "00110"},
    "t2": {"x7": "00111"},
    "s0": {"x8": "01000"},
    "fp": {"x8": "01000"},
    "s1": {"x9": "01001"},
    "a0": {"x10": "01010"},
    "a1": {"x11": "01011"},
    "a2": {"x12": "01100"},
    "a3": {"x13": "01101"},
    "a4": {"x14": "01110"},
    "a5": {"x15": "01111"},
    "a6": {"x16": "10000"},
    "a7": {"x17": "10001"},
    "s2": {"x18": "10010"},
    "s3": {"x19": "10011"},
    "s4": {"x20": "10100"},
    "s5": {"x21": "10101"},
    "s6": {"x22": "10110"},
    "s7": {"x23": "10111"},
    "s8": {"x24": "11000"},
    "s9": {"x25": "11001"},
    "s10": {"x26": "11010"},
    "s11": {"x27": "11011"},
    "t3": {"x28": "11100"},
    "t4": {"x29": "11101"},
    "t5": {"x30": "11110"},
    "t6": {"x31": "11111"},
}

def r_type_instruction(line):
    line = line.strip()
    data1 = line.split(" ")
    data2 = data1[1].split(",")
    if(len(data1)==2 and len(data2)==3 and data1[0] in r_function3.keys() and data2[0] in registers.keys() and data2[1] in registers.keys() and data2[2] in registers.keys()):
        binary=["0000000", str(reg_binary_calc(data2[2])), str(reg_binary_calc(data2[1])), str(r_function3[data1[0]]), str(reg_binary_calc(data2[0])), "0110011"]
        binary1=["0100000", str(reg_binary_calc(data2[2])), str(reg_binary_calc(data2[1])), str(r_function3[data1[0]]), str(reg_binary_calc(data2[0])), "0110011"]

        with open("binary_file.txt", "a") as f:
            if data1[0] == "sub":
                for i in binary1:
                    f.write(i)
                    f.write(" ")
                f.write("\n")
            else:
                for i in binary:
                    f.write(i)
                    f.write(" ")
                f.write("\n")
    else:
        global line_number, flag_of_error
        flag_of_error = True
        with open("binary_file.txt", "w") as f:
                f.write(f"Error generated at line {str(line_number)}")
        

def i_type_instruction(line):
    global line_number, flag_of_error
    l1 = line.split(" ")
    if (len(l1)==2) and (l1[0] in i_opcode.keys()):
        if(l1[0]=="lw" and "(" in l1[1] and ")" in l1[1]):
            to_be_list = l1[1]
            to_be_list = to_be_list.replace("(", ",")
            to_be_list = to_be_list.replace(")", "")
            l2 = to_be_list.split(",")
            l1.pop()
            l1.append(l2)
            if(len(l1[1])==3 and l1[1][0] in registers.keys() and convertible(l1[1][1], 12) and l1[1][2] in registers.keys()):
                instruction = l1[0]
                des = reg_binary_calc(l1[1][0])
                src = reg_binary_calc(l1[1][2])
                imm = int(l1[1][1])
                if(imm<0):
                    imm = binary_rep_compliment(imm, 12)
                else:
                    imm = binary_representation(imm, 12)

                with open("binary_file.txt", "a") as f:
                    f.write(imm + " " + src + " " + i_funct3[instruction] + " " + des + " " + i_opcode[instruction] + "\n")
            else:
                flag_of_error = True
                with open("binary_file.txt", "w") as f:
                    f.write(f"Error generated at line {str(line_number)}")

        elif(l1[0]=="addi" or l1[0]=="sltiu" or l1[0] == "jalr"):
            l2=l1[1].split(",")
            l1.pop()
            l1.append(l2)
            if(len(l1[1])==3 and l1[1][0] in registers.keys() and l1[1][1] in registers.keys() and convertible(l1[1][2], 12)):
                instruction = l1[0]
                des = reg_binary_calc(l1[1][0])
                src = reg_binary_calc(l1[1][1])
                imm = int(l1[1][2])

                if(imm<0):
                    imm = binary_rep_compliment(imm, 12)
                else:
                    imm = binary_representation(imm, 12)

                with open("binary_file.txt", "a") as f:
                    f.write(imm + " " + src + " " + i_funct3[instruction] + " " + des + " " + i_opcode[instruction] + "\n")
            else:
                flag_of_error = True
                with open("binary_file.txt", "w") as f:
                    f.write(f"Error generated at line {str(line_number)}")
        else:
            flag_of_error = True
            with open("binary_file.txt", "w") as f:
                f.write(f"Error generated at line {str(line_number)}")
    else:
        flag_of_error = True
        with open("binary_file.txt", "w") as f:
                f.write(f"Error generated at line {str(line_number)}")

def s_type_instruction(line):
    global line_number, flag_of_error
    if(not("(" in line and ")" in line)):
        with open("binary_file.txt", "w") as f:
            f.write(f"Error generated at line {str(line_number)}")
        return
    
    line = line.replace("(",",")
    line = line.replace(")","")
    line = line.replace(" ",",")

    split_line = line.split(",")

    inst = split_line[0]
    dest_reg = split_line[1]
    reg2 = split_line[3]

    if((inst in s_type) and reg_binary_calc(dest_reg) and convertible(split_line[2], 12) and reg_binary_calc(reg2)):
        imm = int(split_line[2])
        imm = imm_binary_calc(imm)
        print(imm)
        to_write= imm[0:7] + " " + reg_binary_calc(dest_reg) + " " + reg_binary_calc(reg2) + " " + "010" + " " + imm[7:12] + " " + "0100011"
        with open("binary_file.txt","a") as f:
            f.write(to_write)
    else:
        flag_of_error = True
        with open("binary_file.txt", "w") as f:
            f.write(f"Error generated at line {str(line_number)}")

def b_type_instruction():
    pass
def u_type_instruction():
    pass
def j_type_instruction():
    pass

with open("temp.txt") as f:
    for line in f:
        if(flag_of_error==True):
            break
        line_number+=1
        curr_line = line.strip()

        if(line=="\n" or line.isspace()):
            continue
        
        elif(curr_line.split()[0] in r_type):
            r_type_instruction(curr_line)   
            
        elif(curr_line.split()[0] in i_type):
            i_type_instruction(curr_line)
        
        elif(curr_line.split()[0] in s_type):
            s_type_instruction(curr_line)

        elif(curr_line.split()[0] in b_type):
            b_type_instruction()

        elif(curr_line.split()[0] in u_type):
            u_type_instruction()

        elif(curr_line.split()[0] in j_type):
            j_type_instruction()
        
        else:
            flag_of_error = True
            with open("binary_file.txt", "w") as f:
                f.write(f"Error generated at line {str(line_number)}")

