import sys
# encoding for type of commands {1 for registers, -1 for memory address, 0 for immedeate value}
encoding = { "a": [1,1,1], "b": [1,0], "c": [1,1], "d": [1,-1], "e": [-1], "f": []}

# [opcode(bin) : [opcode , number of registers ,immediate value ,memory address, type of command]]
opcode = {"10000" : [ "add", 3, 0 ,0,"a"] , "10001"  : ["sub" , 3 , 0 ,0,"a"] , "10010" : ["mov" , 1 , 1 ,0,"b"],
"10011" : ["mov" , 2 , 0 ,0, "c"], "10100" : ["ld" , 1 , 0 , 1, "d"], "10101" : ["st", 1 , 0 ,1,"d"],
"10110" : ["mul" , 3 , 0,0 ,"a"], "10111" : ["div" , 2 , 0 , 0 , "c"], "11000" : ["rs" , 1 , 1, 0 , "b"],
"11001" : ["ls" , 1 , 1 , 0 , "b"], "11010" : ["xor" , 3 ,0,0 , "a"], "11011" : ["or" , 3 , 0 , 0 , "a"],
"11100" : ["and", 3 , 0 , 0 , "a"], "11101" : ["not" , 2 , 0 , 0 , "c"], "11110" : ["cmp" , 2 , 0 , 0 , "c"],
"11111" : ["jmp" , 0 , 0 , 1 , "e"], "01100" : ["jlt" , 0 , 0 , 1 , "e"], "01101" : ["jgt" , 0 , 0 , 1 , "e"],
"01111" : ["je" , 0 , 0 , 1 , "e"]}

registers=["R0" ,"R1" , "R2" , "R3" , "R4" , "R4" , "R5" , "R6"]
PrintError=0
UpcodeList = []    

def check_op_code(op_list,linenum):
    global PrintError
    
    for x in opcode:
        
        if (opcode[x][0]!=op_list[0]):
            pass
        else:
            if(len(op_list)!=1):
                pass
            else:
                return True
            bind=opcode[x][4]
            if(op_list[0]!="mov"): 
                pass
            else:
                if(op_list[-1]!="FLAGS" and op_list[-1] not in registers):
                    x="10010"
                    bind="b"
                else:
                    x="10011"
                    bind="c"
            res=checkbinding(op_list,bind,linenum)
            op_list=op_list[1:]
            op_list.insert(0,x)
            op_list.append(linenum)
            op_list.append(bind) 
            UpcodeList.append(op_list)
            if(res==True):
                pass
            else:
                print("ERROR at line",linenum,": Wrong syntax used for instructions")
                PrintError=1
            return res
    return False



def checkbinding(op_list,x,linenum):
    enc=encoding[x]
    flag = 0
    if(len(op_list)-1!=len(enc)):
        flag =1
        print("ERROR at line",linenum,": Invalid statement - exceeded number of registers or invalid syntax for a register ") 

    else:
        for i in range(len(enc)):
            if(enc[i]==0): 
                if(op_list[i+1][0]!='$'):   
                    print("ERROR at line",linenum,": Illegal Symbol used for Immediate Value (not a $) ")
                    flag = 1
                    break

                else:
                    if(not op_list[i+1][1:].isdigit()):
                        flag = 1 
                        print("ERROR at line",linenum,": Illegal Immediate Values (Not an integer) ")
                        break
                    else:
                        if(0>int(op_list[i+1][1:])>255):
                            flag = 1
                            print("ERROR at line",linenum,": Illegal Immediate values (less than 0 or more than 255)")
                            break
                        else:
                            continue
                    
            elif(enc[i]==1):  
                if(op_list[i+1]=="FLAGS"):
                    if(op_list[0]!="mov" or i!=(len(enc)-1) or i==1):
                        flag=1
                        print("ERROR at line",linenum,": Illegal use of FLAGS register") 
                        break
                    else:
                        continue
                if(op_list[i+1] in registers):  
                    continue
                else:
                    flag = 1
                    print("ERROR at line",linenum,": Illegal register name ")
                    break                 

            else:
                continue

    if (flag!=1) :
        return True
    else: 
        return False
address_register = {"R0": "000", "R1": "001", "R2": "010","R3": "011", "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}   # dic for register addresses

def _8bit(numstring): # completing 8-digits 
    string_length = 8 - len(numstring)
    if string_length <0:
        print("Number exceeded 8 Bits")
        return None
    else:
        string_final = "0"*string_length
        string_final += numstring
        return string_final
        

def _8bitformat(string): # num $87 , then removing $, converting to binary and then removing the "2b" from starting
    new_string = string[1:]
    new_bin_string = bin(int(new_string))[2:] 
    temp=_8bit(str(new_bin_string))
    if(temp==None):
        return None
    else:
        return temp

VariableLabel={}    # [variable label, line number, MemoryAddress]
MemoryAddress=0     # stores memory address of each line

def getbinary_code(VariableLabel,UpcodeList):
    output  =[]    # list of binarycodes
    j = 0
    while j!=(len(UpcodeList)):
        
        
        if UpcodeList[j][-1]!="a":
            pass
        else:
            P=UpcodeList[j][0]
            Q=address_register[UpcodeList[j][1]]
            R=address_register[UpcodeList[j][2]]
            S=address_register[UpcodeList[j][3]]
            output.append( [P,"00",Q,R,S])
        
        if UpcodeList[j][-1]=="b":
            new_variable=_8bitformat(UpcodeList[j][2])
            if(new_variable==None):
                print("Immedeate value exceeded 8 bits at line",UpcodeList[j][2])  
            else:
                P=UpcodeList[j][0]
                Q=address_register[UpcodeList[j][1]]
                R=new_variable
                output.append([P,Q,R])
                
        if UpcodeList[j][-1]!="c":
            pass
        else:
            P=UpcodeList[j][0]
            Q=address_register[UpcodeList[j][1]]
            R=address_register[UpcodeList[j][2]]
            output.append([P,"00000",Q,R])
        
        if UpcodeList[j][-1]=="d":      
            VariableName=UpcodeList[j][2]
            if(VariableName not in VariableLabel):
                #If use of undefined variables/label then give out error
                print("ERROR at line",UpcodeList[j][-2],": Use of undefined variables")
                output=[-1]
                break
                    
            else:
                if(VariableLabel[VariableName][0]!="variable"):     
                    print("ERROR at line",UpcodeList[j][-2],"Misuse of labels as variable")
                    output=[-1]
                    break
                else:
                    new_variable=_8bit(VariableLabel[UpcodeList[j][2]][2])  
                    if(new_variable==None):
                        print("Immedeate value exceeded 8 bits at line",UpcodeList[j][2])    
                    else: 
                        output.append([ UpcodeList[j][0],address_register[UpcodeList[j][1]], new_variable ] )

        if UpcodeList[j][-1]=="e":
            label_name=UpcodeList[j][1]
            if(label_name not in VariableLabel):
                #If use of undefined variables/label then give out error
                output = [-1]
                print("ERROR at line",UpcodeList[j][-2],": Use of undefined labels")
                break
            else:
                if(VariableLabel[label_name][0]!="label"):      
                    output=[-1]
                    print("ERROR at line",UpcodeList[j][-2],"Misuse of labels as variable")
                    break 
                else:
                    new_variable=_8bit(VariableLabel[UpcodeList[j][1]][2])
                    if(new_variable==None):
                        print("Immedeate value exceeded 8 bits at line",UpcodeList[j][2])
                    else:
                        output.append([ UpcodeList[j][0],"000", new_variable])
                    
        if UpcodeList[j][-1]!="f":     #for halt command
            pass
        else:
            output.append([UpcodeList[j][0],"00000000000"])

        j+=1        
    
    return output

def CheckError(input):      
    global MemoryAddress
    variable=0
    flag=0
    
    for j in range(len(input)-1):
        
        line=input[j]
        if(line=='' or line=='\n'):     
            continue
        line=line.split()
        if(line[0]=="var"):
            if(len(line)!=2):
                print("ERROR at line",j+1,": GENERAL SYNTAX ERROR: Illegal Declaration of variables")
                flag=1
                break        
            else:
                if(variable!=0):
                    print("ERROR at line",j+1,": Variables not declared at the beginning")
                    flag=1
                    break 
                else:
                    VariableName=[]
                    VariableName.append(line[1])
                    if(line[1] in VariableLabel):
                        print("ERROR at line",j+1,": GENERAL SYNTAX ERROR: Label/Variable exists with same name")
                        flag=1
                        break
                    if( check_op_code(VariableName,j+1)):
                        print("ERROR at line",j+1,": GENERAL SYNTAX ERROR: Variable name is an opcode")
                        flag=1
                        break
                    if (((not(line[1].isalnum()) and '_' not in line[1]) or line[1].isdigit()==True)):
                        one = 1
                        flag=one
                        print("ERROR at line",j+1,"GENERAL SYNTAX ERROR: Variable Naming incorrect")
                        break
                    else:
                        VariableLabel[line[1]]=["variable",j,str(bin(len(input)))[2:]]
        elif(line[0][-1]==':'):
            label_name=[]
            label_name.append(line[0][:-1]) 
            variable=1
            if(label_name[0] in VariableLabel):
                flag=1
                print("ERROR at line",j+1,": Label/Variable exists with same name")
                break
            if( check_op_code(label_name,j+1)):
                flag=1
                print("ERROR at line",j+1,": GENERAL SYNTAX ERROR: Label name is opcode")
                break
            if(line[1] == "hlt" and len(line)==2):
                print("ERROR at line",j+1,": hlt not being used as the last instruction")
                flag=1
                break
            elif( check_op_code(line[1:],j+1)):
                VariableLabel[label_name[0]]=["label",j,str(bin(MemoryAddress))[2:]]
                MemoryAddress = MemoryAddress + 1
                continue
            else:
                flag=1
                print("ERROR at line",j+1,": Wrong instruction given at label")
                break
        elif(line[0]=="hlt"):  
            flag=1     
            print("ERROR at line",j+1,": hlt not being used as the last instruction")
            break
        elif( check_op_code(line,j+1)):  
            variable=1
            MemoryAddress=MemoryAddress+1
            continue
        else:
            if( PrintError==1):
                flag=1
                break
            print("ERROR at line",j+1,": Error in opcode/label/variable naming")
            flag=1
            break
        
    return flag

def FirstRun(input):
    last_line=input[-1].split()
    flag=0
    if("hlt" not in last_line):
        flag=1
        print(f"ERROR at line {len(input)}: Missing hlt instruction")
    else:
        if(len(last_line)!=1):
            print("ERROR at line",(len(input)),": Invalid declaration of hlt")
            flag=1
        elif(last_line[0][-1]==":" and len(last_line)==2 ):
            label_name=[]
            label_name.append(last_line[0][:-1])
            if(not  check_op_code(label_name,len(input))):
                VariableLabel[label_name[0]]=["label",len(input)-1,str(bin(MemoryAddress))[2:]]
                flag=CheckError(input)
            else:
                flag=1
                print("ERROR at line",len(input),"Label name is an opcode")
        else:
            flag=CheckError(input)
        UpcodeList.append(["01010","f"])
        
           
        
    if(flag!=0):
        pass
    else:
        var_addr()
    return flag

def var_addr():
    global MemoryAddress
    for j in VariableLabel:
        if(VariableLabel[j][0]!="variable"):
            pass
        else:
            MemoryAddress=MemoryAddress + 1
            VariableLabel[j][2]=str(bin(MemoryAddress))[2:]

def printit(prog_out): 
    for x in prog_out:
        print(''.join(str(i) for i in x))

def main():
    input=[]
    try:
        for line in sys.stdin:      
            input.append(str(line))
    except:
        pass
    end_line=0
    for i in input[::-1]:
        if(i!='' and i!='\n'):
            break
        else:
            end_line +=1
         
    input=input[:len(input)-end_line]
    check = FirstRun(input) 
    if (check!=0):
        print("========PROGRAM TERMINATED========")
    else:
        p=getbinary_code(VariableLabel, UpcodeList)
        if(p!=[-1]):
            printit(p)
        else:
            print("========PROGRAM TERMINATED========")

if __name__ =="__main__":
    main()
