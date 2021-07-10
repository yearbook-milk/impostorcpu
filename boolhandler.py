from memhandler import *

def die(msg):
    input('ImpostorCPU Conditional FATAL: '+msg+'\nPress <ENTER> to exit.')
    exit()
    
def fileio(name, mode, contents = ""): #file io helper
    f = open(name, mode)
    if mode == 'r':
        tr = f.read()
    if mode == 'a' or mode == 'w':
        f.write(contents)
        tr = None
    f.close()
    return tr
    
def inrange(addr):
    if int(addr,16) % 4 == 0 and int(addr,16) > 255 and int(addr,16) < 16777216:
        return True
    else:
        return False
 
def wrapper_byteget(addr):
    nhxa = int(addr, 16)
    if not inrange(addr):
        return getbyte(addr)
    if inrange(addr):
        b1 = getbyte(addr)
        b2 = getbyte(str( hex ( int(addr, 16) + 1 ) )[2:].zfill(8) )
        b3 = getbyte(str( hex ( int(addr, 16) + 2 ) )[2:].zfill(8) )
        b4 = getbyte(str( hex ( int(addr, 16) + 3 ) )[2:].zfill(8) )
        return int(b1+b2+b3+b4, 16) #get bytes and turn them into a number which Python can use
        
def comparison_operation(litaddr, addr1, operation, addr2): #either 8 or 32bit, still do the comparison
    ops = '< > == != <= >='
    opslist = ['>=','>','<=','<','==','!=']
    operation1 = opslist[ int(operation, 16) ]
    if litaddr == '00': #LL
        print('LL COMPARISON')
        op1 = int(addr1, 16)
        op2 = int(addr2, 16)
    if litaddr == '01': #LA
        print('LA COMPARISON')
        op1 = int(addr1, 16)
        op2 = wrapper_byteget(addr2)
    if litaddr == '02': #AL
        print('AL COMPARISON')
        op1 = wrapper_byteget(addr1)
        op2 = int(addr2, 16)
    if litaddr == '03':
        print('AA COMPARISON')
        op1 = wrapper_byteget(addr1)
        op2 = wrapper_byteget(addr2)
    op1 = int(str(op1), 16)
    op2 = int(str(op2), 16)
    print('COMPARE OPERATION',addr1,op1,operation1,addr2,op2)
    
    
    if operation1 not in ops:
        die('Invalid operation '+operation)
        
    if operation1 == '>':
        return op1 > op2
        
    if operation1 == '<':
        return op1 < op2
        
    if operation1 == '>=':
        return op1 >= op2
        
    if operation1 == '<=':
        return op1 <= op2
        
    if operation1 == '==':
        return op1 == op2
        
    if operation1 == '!=':
        return op1 != op2

def intcomop(litaddr,addr1,operation,addr2):
    result = comparison_operation(litaddr,addr1,operation,addr2)
    if result:
        writebyte('00000001', 'FF')
    if not result:
        writebyte('00000001', '00')
        
def logical_operation(litaddr,addr1,operation,addr2):
    ops = ['op1a and op2a','op1a or op2a','(not op1a and op2a) or (op1a and not op2a)','not op1a',]
    print(litaddr,addr1,operation,addr2)
    if litaddr == '00': #LL
        print('LL LOGIC')
        op1 = int(addr1, 16)
        op2 = int(addr2, 16)
    if litaddr == '01': #LA
        print('LA LOGIC')
        op1 = int(addr1, 16)
        op2 = int(getbyte(addr2),16)
    if litaddr == '02': #AL
        print('AL LOGIC')
        op1 = int(getbyte(addr1),16)
        op2 = int(addr2, 16)
    if litaddr == '03':
        print('AA COMPARISON')
        op1 = int(getbyte(addr1),16)
        op2 = int(getbyte(addr2),16)
        
    print(op1,op2)
    if op1 != 0:
        op1a = True
    if op1 == 0:
        op1a = False
        
    if op2 != 0:
        op2a = True
    if op2 == 0:
        op2a = False
    toreturn = 'Error: toreturn not set'
    print(ops[int(operation,16)])
    #print(locals())
    #this function writes to the memory and does not have a return value
    print('LOGICAL COMPARISON',addr1,op1,op1a,ops[int(operation,16)],addr2,op2,op2a)

    exec('res = '+ops[int(operation,16)]+'\nprint("RESULT",res)\nif res == True:\n    writebyte("00000001", "FF")\nelse:\n    writebyte("00000001", "00")')
    print(register)
    return None
#unfinished, need logical AND|OR|XOR|NOT
   
#test  
#writebyte('F0000110', '00')
#input(intcomop('01', '03', '01', 'F0000110'))
#print(register)
#input(intcomop('01', '03', '01', '00000005'))
#print(register)

#writebyte('00000005', 'FF')
#writebyte('F0000005', '00')
#logical_operation('00','00000005','0','F0000005')
#input()
