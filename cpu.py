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
    
def wrapper_4byteget(addr):
    nhxa = int(addr, 16)
    if True:
        b1 = memhandler.getbyte(addr)
        b2 = memhandler.getbyte(str( hex ( int(addr, 16) + 1 ) )[2:].zfill(8) )
        b3 = memhandler.getbyte(str( hex ( int(addr, 16) + 2 ) )[2:].zfill(8) )
        b4 = memhandler.getbyte(str( hex ( int(addr, 16) + 3 ) )[2:].zfill(8) )
        return str(b1+b2+b3+b4).zfill(8)

def inrange(addr):
    if int(addr,16) % 4 == 0 and int(addr,16) > 255 and int(addr,16) < 16777216:
        return True
    else:
        return False
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
                if current_ins[5] == 'FF':
                    execute = True
                else:
                    execute = False

            if current_ins[1] == '01':
                print('Addr',''.join(current_ins[2:6]))
                s = memhandler.getbyte(''.join(current_ins[2:6]))
                print('Value',s)

                if inrange(''.join(current_ins[2:6])):
                    die('Not a valid 8bit slot for result (0xFF or 0x00)')

                if s == 'FF':
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
    
