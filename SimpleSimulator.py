from sys import stdin
import matplotlib.pyplot as plt
hlt = "0101000000000000"
memory = {}
pc = 0
Cycle = -1
x_axis=[]
y_axis=[]
reg_val = {'000': 0, '001': 0, '010': 0, '011': 0, '100': 0, '101': 0, '110': 0, "111": 0}

def _16bitconvertor(n):
    return format(n, "016b")

def _8bitconvertor(n):
    return format(n, "08b")

def get_decimal(binary):
    decimal = 0
    i= 0
    while(binary != 0):
        dec = int(binary) % 10
        decimal = decimal + dec * pow(2, i)
        binary = int(binary)//10
        i += 1
    return int(decimal)

def dump():
    for reg in reg_val.keys():
        print(_16bitconvertor(reg_val[reg]), end=" ")

def flag_reset():
    reg_val["111"] = 0

def plot(): 
    plt.style.use('seaborn')
    plt.scatter(x_axis,y_axis, cmap='YlGnBu', edgecolor='blue', linewidth=1, alpha=0.75)
    plt.xlabel('Cycle number')
    plt.ylabel('Memory address')
    plt.tight_layout()
    plt.show()


inputs=[]

for line in stdin:
    if line=="" or line=="\n":
        pass
    else:
        inputs.append(line.strip())



while (inputs[pc] != hlt):
    Cycle += 1
    print(_8bitconvertor(pc), end=" ")
    command = inputs[pc]
    opcode = command[:5]
    reg = command[5:8]
    imm = get_decimal(command[8:])
    x_axis.append(Cycle)
    y_axis.append(pc)

        
    if (opcode != "10000"):  # add
        pass
    else:
        reg_val[command[13:]] =  reg_val[command[7:10]] + reg_val[command[10:13]]
        if reg_val[command[7:10]] <= 65535:
            flag_reset()
        else:
            reg_val[command[7:10]] = reg_val[command[7:10]] % 65536
            reg_val["111"] = 8
        pc += 1
        
    if (opcode != "10001"):  # sub
        pass
    else:
        reg_val[command[13:]] = reg_val[command[7:10]] - reg_val[command[10:13]] 
        if reg_val[command[7:10]] >= 0:
            flag_reset()
        else:
            reg_val[command[7:10]] = 0
            reg_val["111"] = 8 
        pc += 1
    if (opcode != "10110"):  # mul
        pass
    else:
        reg_val[command[13:]] = reg_val[command[7:10]] * reg_val[command[10:13]]  
        if reg_val[command[7:10]] <= 65535:
            flag_reset()
        else:
            reg_val[command[7:10]] = reg_val[command[7:10]] % 65536
            reg_val["111"] = 8
            
        pc += 1
    
    if (opcode != "11100"): # and
        pass
    else:
        reg_val[command[13:]] = reg_val[command[7:10]] and reg_val[command[10:13]] 
        flag_reset()
        pc += 1
    
    if (opcode != "11010"):  # xor
        pass
    else:
        reg_val[command[13:]] = reg_val[command[7:10]] ^ reg_val[command[10:13]]  
        flag_reset()
        pc += 1
    
    
    if (opcode != "11011"):  # or
        pass
    else:
        reg_val[command[13:]] = reg_val[command[7:10]] or reg_val[command[10:13]]  
        flag_reset()
        pc += 1
    if (opcode != "10010"):  # movi
        pass
    else:
        reg_val[reg] = imm
        flag_reset()
        pc += 1
    if (opcode != "11000"):  # rs
        pass
    else:
        reg_val[reg] = reg_val[reg] >> imm
        flag_reset()
        pc += 1
    if (opcode != "11001"):  # ls
        pass
    else:
        reg_val[reg] = reg_val[reg] << imm
        if reg_val[reg] <= 65535:
            flag_reset()
        else:
            reg_val[reg] = reg_val[reg] % 65536
            reg_val["111"] = 8
            
        pc += 1
    register1 = command[10:13]
    register2 = command[13:]
    if (opcode != "10011"):  # movr
        pass
    else:
        reg_val[register2] = reg_val[register1]
        flag_reset()
        pc += 1
    if (opcode != "10111"):  # divide
        pass
    else:
        reg_val["000"] = reg_val[register1] // reg_val[register2]
        reg_val["001"] = reg_val[register1] % reg_val[register2]
        flag_reset()
        pc += 1
    if (opcode != "11101"):  # invert
        pass
    else:
        reg_val[register2] = 65535 - reg_val[register1]
        flag_reset()
        pc += 1
    if (opcode != "11110"):  # compare
        pass
    else:
        if (reg_val[register1] == reg_val[register2]):
            reg_val["111"] = 1
        elif (reg_val[register1] > reg_val[register2]):
            reg_val["111"] = 2
        elif (reg_val[register1] < reg_val[register2]):
            reg_val["111"] = 4
        pc += 1

    if (opcode != "10100"):  # load
        pass
    else:
        if (command[8:] not in memory.keys()):
            memory[command[8:]] = 0
        reg_val[command[5:8]] = memory[command[8:]]
        mem = int(inputs[pc][8:], 2)
        y_axis.append(mem)
        x_axis.append(Cycle)
        flag_reset()
        pc += 1
    if (opcode != "10101"):  # store
        pass
    else:
        memory[command[8:]] = reg_val[command[5:8]]
        mem = int(inputs[pc][8:], 2)
        y_axis.append(mem)
        x_axis.append(Cycle)
        flag_reset()
        pc += 1
    mem = get_decimal(command[8:])
    if opcode != "11111":  # jmp
        pass
    else:
        flag_reset()
        pc = mem

    if opcode != "01100":  # jlt
        pass
    else:
        if (reg_val["111"] != 4):
            pc += 1
        else:
            pc = mem
            
        flag_reset()
    if opcode != "01101":  # jgt
        pass
    else:
        if (reg_val["111"] != 2):
            pc += 1
        else:
            pc = mem
            
        flag_reset()
    if opcode != "01111":  # je
        pass
    else:
        if (reg_val["111"] != 1):
            pc += 1
        else:
            pc = mem 
        flag_reset()
    dump()
    print()

flag_reset()
print(_8bitconvertor(pc), end=" ")
dump()
y_axis.append(pc)
Cycle += 1
x_axis.append(Cycle)
print()
i=0
while i<256:
    if (i >= len(inputs)):
        j = _8bitconvertor(i)
        if(j in memory.keys()):
            print(_16bitconvertor(memory[j]))
        else:
            print("0000000000000000")
    else:
        print(inputs[i])    
    i+=1
plot()