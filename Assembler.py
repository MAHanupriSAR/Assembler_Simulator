import re
import sys
to_open=sys.argv[1]
towrite=sys.argv[2]
line_number = 0
flag_of_error = False

def imm_binary_calc(imm, max_bits):
    if imm < (-(2**(max_bits-1))) or imm > ((2**(max_bits-1))-1):
        return False
    else:
        binary = ""
        if(imm>=0):
            while imm > 0:
                rem = str(imm % 2)
                binary = rem + binary
                imm //= 2
        else:
            temp = abs(int(pow(2,max_bits)-1) - abs(imm) + 1)
            while temp > 0:
                rem = str(temp % 2)
                binary = rem + binary
                temp //= 2

        if len(binary) < max_bits:
            if imm < 0:
                binary = "1" * (max_bits - len(binary)) + binary
            else:
                binary = "0" * (max_bits - len(binary)) + binary
        return binary

def is_continuous_alphabets(substring):
    pattern = r'^[a-zA-Z0-9_]+$'
    if re.match(pattern, substring):
        return True
    else:
        return False

def reg_binary_calc(register_name):
    if register_name in registers:
        return list(registers[register_name].values())[0]
    else:
        for register, values in registers.items():
            if register_name in values:
                return values[register_name] 
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
u_opcode = {"auipc":"0010111", "lui":"0110111"}
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

        with open(towrite, "a") as f:
            if data1[0] == "sub":
                for i in binary1:
                    f.write(i)
                f.write("\n")
            else:
                for i in binary:
                    f.write(i)
                f.write("\n")
    else:
        global line_number, flag_of_error
        flag_of_error = True
        with open(towrite, "w") as f:
                f.write("")
        print(f"Error generated at line {str(line_number)}")
        

def i_type_instruction(line):
    global line_number, flag_of_error
    l1 = line.split(" ")
    if (len(l1)==2) and (l1[0] == "lw"):
        pattern = r'^lw [a-zA-Z0-9]+,[-]?\d+\([a-zA-Z0-9]+\)$'
        if(not re.match(pattern, line)):
            flag_of_error = True
            with open(towrite, "w") as f:
                f.write("")
            print(f"Error generated at line {str(line_number)}")
            return
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

            with open(towrite, "a") as f:
                f.write(imm + src + i_funct3[instruction] + des + i_opcode[instruction] + "\n")
        else:
            flag_of_error = True
            with open(towrite, "w") as f:
                f.write("")
            print(f"Error generated at line {str(line_number)}")

    elif((len(l1)==2) and (l1[0]=="addi" or l1[0]=="sltiu" or l1[0] == "jalr")):
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

            with open(towrite, "a") as f:
                f.write(imm + src + i_funct3[instruction] + des + i_opcode[instruction] + "\n")
        else:
            flag_of_error = True
            with open(towrite, "w") as f:
                f.write("")
            print(f"Error generated at line {str(line_number)}")
    else:
        flag_of_error = True
        with open(towrite, "w") as f:
            f.write("")
        print(f"Error generated at line {str(line_number)}")
        

def s_type_instruction(line):
    global line_number, flag_of_error
    pattern = r'^sw [a-zA-Z0-9]+,[-]?\d+\([a-zA-Z0-9]+\)$'
    if(not re.match(pattern, line)):
        flag_of_error = True
        with open(towrite, "w") as f:
            f.write("")
        print(f"Error generated at line {str(line_number)}")
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
        imm = imm_binary_calc(imm, 12)
        to_write= imm[0:7] + reg_binary_calc(dest_reg) + reg_binary_calc(reg2) + "010" + imm[7:12] + "0100011" + "\n"
        with open(towrite,"a") as f:
            f.write(to_write)
    else:
        flag_of_error = True
        with open(towrite, "w") as f:
            f.write("")
        print(f"Error generated at line {str(line_number)}")

def b_type_instruction(line):
    global line_number, flag_of_error
    pattern = r'^(beq|bne|blt|bge|bltu|bgeu) [a-zA-Z0-9]+,[a-zA-Z0-9]+,[-]?\d+$'
    if(not re.match(pattern, line)):
        flag_of_error = True
        with open(towrite, "w") as f:
            f.write("")
        print(f"Error generated at line {str(line_number)}")
        return
    
    inst_funct3 = {"beq":"000", "bne":"001", "blt":"100", "bge":"101", "bltu":"110", "bgeu":"111"}
    line = line.replace(" ", ",")
    split_line = line.split(",")
    inst = split_line[0]
    rs1 = split_line[1]
    rs2 = split_line[2]

    if((inst in b_type) and reg_binary_calc(rs1) and reg_binary_calc(rs2) and convertible(split_line[3], 16)):
        imm = int(split_line[3])
        imm = imm_binary_calc(imm, 16)
        to_write = imm[3]+imm[5:11] + reg_binary_calc(rs2) + reg_binary_calc(rs1) + inst_funct3[inst] + imm[11:15]+imm[4] + "1100011" + "\n"
        with open(towrite,"a") as f:
            f.write(to_write)
    else:
        flag_of_error = True
        with open(towrite, "w") as f:
            f.write("")
        print(f"Error generated at line {str(line_number)}")
            
def u_type_instruction(line):
    global line_number, flag_of_error
    pattern = r'^(auipc|lui) [a-zA-Z0-9]+,?[-]?\d+$'
    if(not re.match(pattern, line)):
        flag_of_error = True
        with open(towrite, "w") as f:
            f.write("")
        print(f"Error generated at line {str(line_number)}")
        return
    line = line.replace(" ", ",")
    l1 = line.split(",")
    if(len(l1)==3 and l1[0] in u_opcode.keys() and l1[1] in registers.keys() and convertible(l1[2], 32)):
        instruction = u_opcode[l1[0]]
        des = reg_binary_calc(l1[1])
        imm = int(l1[2])

        if(imm<0):
            imm = str(binary_rep_compliment(imm, 32))
        else:
            imm = str(binary_representation(imm, 32))
        
        imm_to_be_stored = imm[0:20]

        with open(towrite, "a") as f:
            f.write(f"{imm_to_be_stored}{des}{instruction}\n")
    else:
        flag_of_error = True
        with open(towrite, "w") as f:
            f.write("")
        print(f"Error generated at line {str(line_number)}")
        return

def j_type_instruction(line):
    global line_number, flag_of_error
    pattern = r'^jal [a-zA-Z0-9]+,[-]?\d+$'
    opcode="1101111"
    line1=line.split()
    if(not re.match(pattern, line)):
        flag_of_error=True
        with open(towrite, "w") as f:
            f.write("") 
        print(f"Error generated at line {str(line_number)}")
    else:
        if(len(line1)==2 and line1[0]=='jal'):
                line2=line1[1].split(",")
                if(line2[0] in registers.keys() and convertible((line2[1]),21)):
                    reg=str(reg_binary_calc(line2[0]))
                    imm=str(imm_binary_calc(int(line2[1]),21))
                    imm=imm[::-1]
                    imm_1=''
                    imm_3=''
                    for index,i in enumerate(imm,start=0):
                        if 11 < index < 20:  
                            imm_1 += str(i)
                            
                        elif 0 < index < 11:  
                            imm_3 += str(i)
                            
                    imm_1=imm_1[::-1]  
                    imm_3=imm_3[::-1]    
                    imm_2=str(imm[10])
                    imm_4=str(imm[19])
                    imm_mod=imm_4+imm_3+imm_2+imm_1
                    with open(towrite, "a") as f:
                        f.write(f"{imm_mod}{reg}{opcode}\n")
                else:
                    flag_of_error=True
                    with open(towrite, "w") as f:
                        f.write("")
                    print(f"Error generated at line {str(line_number)}")
        else:
                flag_of_error=True
                with open(towrite,'w') as f:
                    f.write("")
                print(f"Error generated at line {str(line_number)}")

line_no = 0
label_list = []
with open(to_open) as f:
    for line in f:
        line_no += 1
        address = line_no*4
        label = ""
        i=0
        if(":" in line):
            for i in range(len(line)):
                if (line[i]==":"):
                    break
                label += line[i]
            label_list.append({label:line_no})

text1 = ""
with open(to_open) as f:
    for line in f:
        text1 += line

# or (line[line.index(char) + 1] != " "

line_num=0
text = ""
char = ":"
with open(to_open) as f:
    for line in f:
        line_num+=1
        if(char in line):
            if((not (is_continuous_alphabets(line[:line.index(char)])))):
                with open(towrite, "w") as fh:
                    fh.write("")
                print(f"Error generated at line {str(line_num)}")
                flag_of_error=True
                break
            line = line[line.index(char)+1:]
        for elements in label_list:
            la = (list(elements.keys()))[0]
            ln = (list(elements.values()))[0]
            if la in line:
                line = line.replace(str(la), str((ln-line_num)*4))
        text += line

with open(to_open, "w") as f:
    f.write(text)

main_list = [0,0]                 
halt = "beq zero,zero,0"
with open(to_open) as f:
    for line in f:
        if(flag_of_error==True):
            break
        line_number+=1
        curr_line = line.strip()

        if(line=="\n" or line.isspace()):
            continue

        elif (curr_line==halt):
            b_type_instruction(curr_line)
            main_list[1] = line_number
            main_list[0] = line_number
        
        elif(curr_line.split()[0] in r_type):
            main_list[1] = line_number
            r_type_instruction(curr_line)   
            
        elif(curr_line.split()[0] in i_type):
            main_list[1] = line_number
            i_type_instruction(curr_line)
        
        elif(curr_line.split()[0] in s_type):
            main_list[1] = line_number
            s_type_instruction(curr_line)

        elif(curr_line.split()[0] in b_type):
            main_list[1] = line_number
            b_type_instruction(curr_line)

        elif(curr_line.split()[0] in u_type):
            main_list[1] = line_number
            u_type_instruction(curr_line)

        elif(curr_line.split()[0] in j_type):
            main_list[1] = line_number
            j_type_instruction(curr_line)
        
        else:
            flag_of_error = True
            with open(towrite, "w") as f:
                f.write("")
            print(f"Error generated at line {str(line_number)}")

# if(flag_of_error==False):
#     with open(towrite, "a") as f:
#         f.write(f"00000000000000000000000001100011")

if(flag_of_error==False):
    if(main_list[0]==0):
        with open(towrite, "w") as f:
            f.write("")
        print("Virtual halt absent")
    elif(len(main_list)==2):
        if(main_list[0] != main_list[1]):
            with open(towrite, "w") as f:
                f.write("")
            print(f"Error generated as virtual halt is on line {main_list[0]} and last instruction is on line {main_list[1]}")

with open(to_open, "w") as f:
    f.write(text1)
