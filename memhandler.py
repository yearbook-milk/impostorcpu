#this script is responsible for handling memory and registers
#this script converts the base 16 addresses into integer addresses
#for checking if they are 4byte or 1byte sector, but otherwise, all operations use the hex address.
mininum_hex4byte = 256
maxinum_hex4byte = 16777216
register = {
'00000000': None,
'00000001': None,
'00000002': None,
'00000003': None,
'00000004': None,
'00000005': None,
'00000006': None,
'00000007': None,
'00000008': None,
'00000009': None,
'0000000A': None,
'0000000B': None,
'0000000C': None,
'0000000D': None,
'0000000E': None,
'0000000F': None,
}

def fileio(name, mode, contents = ""): #file io helper
    f = open(name, mode)
    if mode == 'r':
        tr = f.read()
    if mode == 'a' or mode == 'w':
        f.write(contents)
        tr = None
    f.close()
    return tr

#clear mem
fileio('memory.txt', 'w', '')

def die(msg):
    input('ImpostorCPU Mem FATAL: '+msg+'\nPress <ENTER> to exit.')
    exit()
    
    
def getbyte(addr): #take hex address and get the thing
    #print('Addrget',addr)
    nhex_addr = int(str(addr),16)
    if nhex_addr < 16 and register[addr] != None:
        return str(register[addr])
    if nhex_addr < 16 and register[addr] == None:
        die('Register value '+addr+' does not exist.')
    else:
        xcn = fileio('memory.txt', 'r')
        offset = xcn.find(str(addr))
        #print(offset)
        #print(addr)
        if offset >= 0:
            return xcn[offset+len(str(addr))+1:offset+len(str(addr))+3]
        else:
            die('Address '+str(addr)+' is invalid.')
        
def writebyte(addr, byte): #take hex address and byte and write to mem, if already exist then overwrite
    nhex_addr = int(str(addr), 16)
    nhex_m4 = nhex_addr % 4 == 0
    nhex_ir = nhex_addr >= 256 and nhex_addr < 16777216
    
    if nhex_addr > 16:
        news = str(addr)+' '+str(byte)+'\n'
        newsa = fileio('memory.txt', 'r')
        if newsa.count(addr) > 0:
            print('OVER-WRITE',addr,byte)
            newsa = newsa.replace( addr+' '+getbyte(addr)+'\n' , news )
        else:
            print('WRITE',addr,byte)
            newsa = newsa + news
        
            
        n = fileio('memory.txt', 'w', newsa)
        
    if nhex_addr <= 16:
        register[addr] = byte
        print('Set register',addr,'to',byte)

    if nhex_ir and nhex_m4 and nhex_addr > 16:
        print('ImpostorCPU Warning - Unless being controlled by method writefourbyte, invalid address space for addr',addr)

def writefourbyte(addr,byte1,byte2,byte3,byte4):
    nhex_addr = int(addr, 16)
    nhex_m4 = nhex_addr % 4 == 0
    nhex_ir = nhex_addr >= 256 and nhex_addr < 16777216
    hexobj = '0x'+addr

    if nhex_ir and nhex_m4 and nhex_addr > 16:
        addr1 = nhex_addr
        addr2 = nhex_addr + 1
        addr3 = nhex_addr + 2
        addr4 = nhex_addr + 3

        writebyte( str(hex(addr1))[2:].zfill(8).upper(), byte1 )
        writebyte( str(hex(addr2))[2:].zfill(8).upper(), byte2 )
        writebyte( str(hex(addr3))[2:].zfill(8).upper(), byte3 )
        writebyte( str(hex(addr4))[2:].zfill(8).upper(), byte4 )
    if not nhex_ir or not nhex_m4:
        die('Invalid memory address for 32bit write operation @ addr',addr)

    #print('FOURBYTE WRITE ',addr1,byte1,addr2,byte2,addr3,byte3,addr4,byte4)

    if nhex_ir and not nhex_m4 and nhex_addr > 16:
        die('Invalid memory address for fourbyte sector @ addr '+addr)



def copybyte(addr1, addr2): #copy bytes from addr1 to addr2
    nhex_addr = int(addr1, 16)
    nhex_addr2 = int(addr2, 16)

    nhex_m4 = nhex_addr % 4 == 0
    nhex_ir = nhex_addr >= 256 and nhex_addr < 16777216

    nhex1_m4 = nhex_addr2 % 4 == 0
    nhex1_ir = nhex_addr2 >= 256 and nhex_addr2 < 16777216

    #print(nhex_m4,nhex_ir,nhex1_m4,nhex1_ir)

    #if its a fourbyte address
    if nhex_m4 and nhex_ir and nhex1_m4 and nhex1_ir:
        print('COPY',addr1,nhex_addr,addr2,nhex_addr2,'[+4]')
        tocopy = range(nhex_addr, nhex_addr+4)
        destinationbytes = range(nhex_addr2, nhex_addr2+4)
        i = 0
        writebyte( str( hex(destinationbytes[i]) )[2:].zfill(8).upper() , getbyte( str(hex(tocopy[i]))[2:].zfill(8) ))
        print( str( hex(destinationbytes[i]) )[2:].zfill(8).upper() , getbyte(str(hex(tocopy[i]))[2:].zfill(8)))
        i = 1
        writebyte( str( hex(destinationbytes[i]) )[2:].zfill(8).upper() , getbyte(str(hex(tocopy[i]))[2:].zfill(8)))
        print( str( hex(destinationbytes[i]) )[2:].zfill(8).upper() , getbyte(str(hex(tocopy[i]))[2:].zfill(8)))
        i = 2
        writebyte( str( hex(destinationbytes[i]) )[2:].zfill(8).upper() , getbyte(str(hex(tocopy[i]))[2:].zfill(8)))
        print( str( hex(destinationbytes[i]) )[2:].zfill(8).upper() , getbyte(str(hex(tocopy[i]))[2:].zfill(8)))
        i = 3
        writebyte( str( hex(destinationbytes[i]) )[2:].zfill(8).upper() , getbyte(str(hex(tocopy[i]))[2:].zfill(8)))
        print( str( hex(destinationbytes[i]) )[2:].zfill(8).upper() , getbyte(str(hex(tocopy[i]))[2:].zfill(8)))
    elif not nhex_m4 or not nhex1_m4:
        die('Invalid memory address for fourbyte sector @ addrs '+addr1+' '+addr2)
    else:
        #if its just one byte to copy
        print('COPY',addr1,nhex_addr,addr2,nhex_addr2,'[1]')
        writebyte( str(addr2), getbyte( str(addr1) ) )
        print(addr1,addr2,getbyte(str(addr1)))

#test
#writefourbyte('00000200','AB','CD','EF','01')
#writefourbyte('00000200','AB','CD','01','01')
#copybyte('00000200','0000020C')

#writebyte('00000004', 'FF')
#print(register)
