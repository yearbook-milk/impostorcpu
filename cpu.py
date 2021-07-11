#this script handles reading instructions and starting their executions
import memhandler
import mathshandler
import boolhandler
print('ImpostorCPU :: beginning of execution')
#preparation
def fileio(name, mode, contents = ""):
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

def setreturn(statement):
    if statement:
        memhandler.writebyte('00000001', 'FF')
        print('write true')
    else:
        memhandler.writebyte('00000001', '00')
        print('write false')
        
def wrapper_4byteget(addr):
    nhxa = int(addr, 16)
    print('Inrange ',addr, inrange(addr) )
    if inrange(addr):
        b1 = memhandler.getbyte(addr)
        b2 = memhandler.getbyte(str( hex ( int(addr, 16) + 1 ) )[2:].zfill(8) )
        b3 = memhandler.getbyte(str( hex ( int(addr, 16) + 2 ) )[2:].zfill(8) )
        b4 = memhandler.getbyte(str( hex ( int(addr, 16) + 3 ) )[2:].zfill(8) )
        return str(b1+b2+b3+b4).zfill(8)
    if not inrange(addr):
        print('Val Non32',memhandler.getbyte(addr))
        return memhandler.getbyte(addr)
        
def die(msg):
    input('ImpostorCPU Main FATAL: '+msg+'\nPress <ENTER> to exit.')
    exit()

bytess = fileio('bios.txt','r').replace(' ', '').replace('{','').replace('}','').replace('\n','')
bytelist = []
for index in range(0, len(bytess), 2):
    bytelist.append(bytess[index : index + 2])
print(bytelist)

#the actual program
def execute_program(startaddr):
    nonhexaddr = int(startaddr, 16)
    keepon = True
    memhandler.writebyte('00000005',startaddr) #the program ticker
    print(memhandler.register)
    current_ins = []

    while keepon:
        for i in range(0, 11):
            current_ins.append(memhandler.getbyte(memhandler.getbyte('00000005'))) #get an 11 byte set of instructions
            nonhexaddr = nonhexaddr + 1
            memhandler.writebyte('00000005', str(hex(nonhexaddr))[2:].zfill(8).upper() )
        print('On instruction',current_ins)
        #print('Not going to do anything, that comes later.')

        #some meta commands
        if current_ins[0] == '0D':
            print('Program terminated with 0D command')
            keepon = False
            return None
        elif current_ins[0] == '0E':
            print('MEMORY:\n',fileio('memory.txt','r'),'REGISTERS:\n',memhandler.register)
            current_ins = [] # clear the ins list for next ins (11byte)
        elif current_ins[0] == '0B':
            die('0B is not a valid command')
            
        #jump handling
            
        elif current_ins[0] == '06': #write the address of the current instruction to an address
            addrto = ''.join(current_ins[3:7])
            print('Destination address:',addrto)
            print('Current address:',memhandler.getbyte('00000005'))
            adlist = memhandler.getbyte('00000005')
            print('SFP',adlist[0:2],adlist[2:4],adlist[4:6],adlist[6:8])
            
            if inrange(addrto):
                memhandler.writefourbyte(addrto,adlist[0:2],adlist[2:4],adlist[4:6],adlist[6:8])
                print('Value of',addrto)
                #print('MEMORY:\n',fileio('memory.txt','r'),'REGISTERS:\n',memhandler.register)
            if not inrange(addrto):
                die('Not a valid 32bit mem slot')
        elif current_ins[0] == '0C': # make a literal jump
            memhandler.writebyte('00000005', ''.join(current_ins[1:5]))
            nonhexaddr = int(''.join(current_ins[1:5]), 16)
            print('New Instruction Address:',''.join(current_ins[1:5]))
            print('Made jump to',nonhexaddr,''.join(current_ins[1:5]))
        elif current_ins[0] == '07': #read addr and jump to what was there
            print('Readfrom',current_ins[1:5])
            readaddr = wrapper_4byteget(''.join(current_ins[1:5]))
            print('Got',readaddr,'from',''.join(current_ins[1:5]))
            nonhexaddr = int(readaddr, 16)
            memhandler.writebyte('00000005', readaddr)


        #if handling

        elif current_ins[0] == '0A':
            execute = False
            print('OLD',memhandler.getbyte('00000005'), int(memhandler.getbyte('00000005'),16))
            #test
            #memhandler.writebyte('00000001', 'FF')
            #test
            
            if current_ins[1] == '00':
                print('Literal byte',current_ins[5])
                if current_ins[5] != '00':
                    execute = True
                else:
                    execute = False

            if current_ins[1] == '01':
                print('Addr',''.join(current_ins[2:6]))
                s = memhandler.getbyte(''.join(current_ins[2:6]))
                print('Value',s)

                if inrange(''.join(current_ins[2:6])):
                    die('Not a valid 8bit slot for result (0xFF or 0x00)')

                if s != '00':
                    execute = True
                else:
                    execute = False

            print('To execute:',execute)
            print('Number of instructions to skip or do:',''.join(current_ins[6:10]))

            if execute:
                pass #do nothing, let the program counter move on to the next instructions
            if not execute:
                nonhexaddr = int(memhandler.getbyte('00000005'), 16) + (int(''.join(current_ins[6:10]) , 16) * 11) - 11 #current + jump*11 
                memhandler.writebyte('00000005', str(hex(nonhexaddr + 1))[2:].zfill(8).upper() ) #hexlify the new addr
                print('New addr:',str(hex(nonhexaddr + 1))[2:].zfill(8).upper(),nonhexaddr)
        elif current_ins[0] == '08':

            #test
            #memhandler.writebyte('00000007','FF')
            #write to 00000001 the operation
            #test
            
            if current_ins[1] == '00': # LL
                int1 = int(str(''.join(current_ins[2:6])), 16)
                print('Operator 1',int1,''.join(current_ins[2:6]))
                
                int2 = int(str(''.join(current_ins[7:])), 16)
                print('Operator 2',int2,''.join(current_ins[7:]))

            if current_ins[1] == '01': #LA
                int1 = int(str(''.join(current_ins[2:6])), 16)
                print('Operator 1',int1,''.join(current_ins[2:6]))

                int2 = int(wrapper_4byteget(''.join(current_ins[7:]) ),16)
                print('Mem Operator 2',int2,''.join(current_ins[7:]) )

            if current_ins[1] == '02': #AL
                int1 = int(wrapper_4byteget(''.join(current_ins[2:6]) ),16)
                print('Mem Operator 1',int1,''.join(current_ins[2:6]))

                int2 = int(''.join(current_ins[7:]), 16)
                print('Operator 2',int2,''.join(current_ins[7:]))

            if current_ins[1] == '03': # AA
                int1 = int(wrapper_4byteget(''.join(current_ins[2:6]) ),16)
                print('Mem Operator 1',int1,''.join(current_ins[2:6]))

                int2 = int(wrapper_4byteget(''.join(current_ins[7:]) ),16)
                print('Mem Operator 2',int1,''.join(current_ins[7:]))

            ops = {'00': '>=', '01': '>', '02': '<=', '03': '<', '04': '==', '05': '!='}
            print('setreturn('+str(int1)+ops[current_ins[6]]+str(int2)+')')
            exec('setreturn('+str(int1)+ops[current_ins[6]]+str(int2)+')')
            print(memhandler.register)

        elif current_ins[0] == '09':
            #logicals (FF and 00, FF xor FF, etc.)

            #test
            #memhandler.writebyte('00000007','01')
            #test

            print('LL/AA byte',current_ins[1])
            print('addr1',''.join(current_ins[2:6]))
            print('opbyte',current_ins[6])
            print('addr2',''.join(current_ins[7:11]))
            boolhandler.logical_operation(current_ins[1],''.join(current_ins[2:6]),current_ins[6],''.join(current_ins[7:11]))
            print(memhandler.register)


        #memory operations

        #test
        #memhandler.writebyte('99ABCD42', 'F4')
        #test
        
        elif current_ins[0] == '00':
            #memhandler.writebyte('99ABCD42', 'F4')
            #memhandler.writefourbyte('00000104', 'F4','31','31','25')
            contents = None
            contents = wrapper_4byteget(''.join(current_ins[3:7]))
            print('Addr1:',contents,current_ins[3:7])
            print('Addr2:',current_ins[7:11])

            if len(contents) == 2:
                memhandler.writebyte(''.join(current_ins[7:11]), contents)
                print('00 non32 Copy contents')
            else:
                memhandler.writefourbyte(''.join(current_ins[7:11]), contents[0:2], contents[2:4], contents[4:6], contents[6:8])
                print('00 Copy',contents[0:2], contents[2:4], contents[4:6], contents[6:8])

        elif current_ins[0] == '01' and current_ins[1] == '00': #for writing a literal, the other option is delete
            if inrange(''.join(current_ins[3:7])):
                memhandler.writefourbyte(''.join(current_ins[3:7]), current_ins[7], current_ins[8], current_ins[9], current_ins[10])
                print('01 00 Command 32',''.join(current_ins[3:7]), current_ins[7], current_ins[8], current_ins[9], current_ins[10])
            else:
                memhandler.writebyte(''.join(current_ins[3:7]), current_ins[10])

        elif current_ins[0] == '01' and current_ins[1] == '01':
            if inrange(''.join(current_ins[3:7])):
                f = open('memory.txt', 'r')
                s = f.read()
                f.close()

                nhex_addr = int(''.join(current_ins[3:7]), 16)
                print(str(hex(nhex_addr + 1))[2:].upper().zfill(8) + ' ' + memhandler.getbyte(''.join(current_ins[3:7])) + '\n')

                s = s.replace(''.join(current_ins[3:7]) + ' ' + memhandler.getbyte(''.join(current_ins[3:7])) + '', '')
                s = s.replace(str(hex(nhex_addr + 1))[2:].upper().zfill(8) + ' ' + memhandler.getbyte(''.join(current_ins[3:7])) + '', '')
                s = s.replace(str(hex(nhex_addr + 2))[2:].upper().zfill(8) + ' ' + memhandler.getbyte(''.join(current_ins[3:7])) + '', '')
                s = s.replace(str(hex(nhex_addr + 3))[2:].upper().zfill(8) + ' ' + memhandler.getbyte(''.join(current_ins[3:7])) + '', '')

                fileio('memory.txt','w',s)    
                                
            else:
                f = open('memory.txt', 'r')
                s = f.read().replace(''.join(current_ins[3:7])+' '+memhandler.getbyte(''.join(current_ins[3:7]))+'\n', '' )
                f.close()
                fileio('memory.txt','w',s)                                   

        
        current_ins = []

#load instructions
addr = 'A0000000'
naddr = 2684354560
for i in bytelist:
    memhandler.writebyte(addr, i)
    print('Loaded byte',i,'into memaddr',addr)
    addr = str(hex(naddr + 1))[2:].zfill(8).upper()
    naddr = naddr + 1
    
#input('ImpostorCPU: Ready to begin execution of instructions loaded into memory - <ENTER> to go')
execute_program('A0000000')
input('ImpostorCPU :: end of execution')
    
