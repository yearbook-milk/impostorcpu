from memhandler import *
ops = '+-/*'
def fileio(name, mode, contents = ""): #file io helper
    f = open(name, mode)
    if mode == 'r':
        tr = f.read()
    if mode == 'a' or mode == 'w':
        f.write(contents)
        tr = None
    f.close()
    return tr

def die(msg):
    input('ImpostorCPU Math FATAL: '+msg+'\nPress <ENTER> to exit.')
    exit()

def operation_32bit(memaddress0, mode, operation, secondop): #an operation on memory with addresses in the 32bit area
    ad1 = getbyte(str(memaddress0))
    ad2 = getbyte(str( hex ( int(memaddress0, 16) + 1 ) )[2:].zfill(8).upper() )
    ad3 = getbyte(str( hex ( int(memaddress0, 16) + 2 ) )[2:].zfill(8).upper() )
    ad4 = getbyte(str( hex ( int(memaddress0, 16) + 3 ) )[2:].zfill(8).upper() )
    firstop = int(ad1+ad2+ad3+ad4, 16)
    print('32BIT INTMATH FIRSTOP','HEXNO',ad1+ad2+ad3+ad4,'INTNO',firstop)

    if mode == 'LITERAL': #just convert to decimal
        secondopreal = int(secondop, 16)
        print('32BIT INTMATH SECONDOP HEXNO',secondop,'INTNO',secondopreal)
    if mode == 'ADDRESS': #get the bytes from memory then combine and decint them
        sad1 = getbyte(str(secondop))
        sad2 = getbyte(str( hex ( int(secondop, 16) + 1 ) )[2:].zfill(8).upper() ) #get the next four addresses
        sad3 = getbyte(str( hex ( int(secondop, 16) + 2 ) )[2:].zfill(8).upper() )
        sad4 = getbyte(str( hex ( int(secondop, 16) + 3 ) )[2:].zfill(8).upper() )
        secondopreal = int(sad1+sad2+sad3+sad4, 16) #convert the bytes from memory into decint
        print('32BIT INTMATH SECONDOP HEXNO',sad1+sad2+sad3+sad4,'INTNO',secondopreal)
    if mode != 'ADDRESS' and mode != 'LITERAL':
        die('Invalid source mode: '+mode)

    global ops

    if operation not in ops:
        die('Invalid operation: '+operation)

    if operation == '+':
        answer = firstop + secondopreal
        answerhex = hex(answer)[2:].zfill(8).upper() #remove 0x and add 0s
        if int(answerhex, 16) > int('FFFFFFFF', 16) or int(answerhex,16) < 0:
            die('ADD Integer overflow @ intanswer '+str(answer)+' hexanswer '+str(answerhex))
        writefourbyte(memaddress0, answerhex[0:2], answerhex[2:4], answerhex[4:6], answerhex[6:8] )
        print(answerhex[6:8])
        print('32BIT INTMATH INTANS',answer,'HEXANS',answerhex)

    if operation == '-':
        answer = firstop - secondopreal
        answerhex = hex(answer)[2:].zfill(8).upper() #remove 0x and add 0s
        if int(answerhex, 16) > int('FFFFFFFF', 16) or int(answerhex,16) < 0:
            die('SUB Integer overflow @ intanswer '+str(answer)+' hexanswer '+str(answerhex))
        writefourbyte(memaddress0, answerhex[0:2], answerhex[2:4], answerhex[4:6], answerhex[6:8] )
        print(answerhex[6:8])
        print('32BIT INTMATH INTANS',answer,'HEXANS',answerhex)

    if operation == '*':
        answer = firstop * secondopreal
        answerhex = hex(answer)[2:].zfill(8).upper() #remove 0x and add 0s
        if int(answerhex, 16) > int('FFFFFFFF', 16) or int(answerhex,16) < 0:
            die('Integer overflow @ intanswer '+str(answer)+' hexanswer '+str(answerhex))
        writefourbyte(memaddress0, answerhex[0:2], answerhex[2:4], answerhex[4:6], answerhex[6:8] )
        print(answerhex[6:8])
        print('32BIT INTMATH INTANS',answer,'HEXANS',answerhex)

    if operation == '/': #use python built in floor division
        answer = firstop // secondopreal
        answerhex = hex(answer)[2:].zfill(8).upper() #remove 0x and add 0s
        if int(answerhex, 16) > int('FFFFFFFF', 16) or int(answerhex,16) < 0:
            die('Integer overflow @ intanswer '+str(answer)+' hexanswer '+str(answerhex))
        writefourbyte(memaddress0, answerhex[0:2], answerhex[2:4], answerhex[4:6], answerhex[6:8] )
        print(answerhex[6:8])
        print('32BIT INTMATH INTANS',answer,'HEXANS',answerhex)

def eightbit_operation(memaddress0, mode, operation, secondop):
    firstop = int(getbyte(memaddress0), 16)
    if mode == 'LITERAL':
        secondopreal = int(secondop, 16) #convert literal second to decint
    if mode == 'ADDRESS':
        secondopreal = int(getbyte(secondop),16) #get byte from mem and convert
    if mode != 'ADDRESS' and mode != 'LITERAL':
        die('Invalid source mode: '+mode)

    print('1BYTE INTMATH INT FIRSTOP',firstop,'SECONDOP',secondopreal)
        
    global ops
    if operation not in ops:
        die('Invalid operation: '+operation)

    if operation == '+':
        answer = firstop + secondopreal
        answerhex = hex(answer)[2:].zfill(2).upper()

        if int(answerhex, 16) > int('FF', 16) or int(answerhex,16) < 0:
            die('Integer overflow @ intanswer '+str(answer)+' hexanswer '+str(answerhex))
        print('1BYTE INTMATH INTANS',answer,'HEXANS',answerhex)
        writebyte(memaddress0, answerhex)
    if operation == '-':
        answer = firstop - secondopreal
        answerhex = hex(answer)[2:].zfill(2).upper()

        if int(answerhex, 16) > int('FF', 16) or int(answerhex,16) < 0:
            die('Integer overflow @ intanswer '+str(answer)+' hexanswer '+str(answerhex))
        print('1BYTE INTMATH INTANS',answer,'HEXANS',answerhex)
        writebyte(memaddress0, answerhex)
    if operation == '*':
        answer = firstop * secondopreal
        answerhex = hex(answer)[2:].zfill(2).upper()

        if int(answerhex, 16) > int('FF', 16) or int(answerhex,16) < 0:
            die('Integer overflow @ intanswer '+str(answer)+' hexanswer '+str(answerhex))
        print('1BYTE INTMATH INTANS',answer,'HEXANS',answerhex)
        writebyte(memaddress0, answerhex)
    if operation == '/':
        answer = firstop // secondopreal
        answerhex = hex(answer)[2:].zfill(2).upper()

        if int(answerhex, 16) > int('FF', 16) or int(answerhex,16) < 0:
            die('Integer overflow @ intanswer '+str(answer)+' hexanswer '+str(answerhex))
        print('1BYTE INTMATH INTANS',answer,'HEXANS',answerhex)
        writebyte(memaddress0, answerhex)

    
#test
#writebyte('0A001111', '44')
#eightbit_operation('0A001111', 'LITERAL', '+', 'F')
