import memhandler as mem
import monitor_api as mapi

addr1 = '00000104'
addr2 = '00000108'
singl = 'D000000A'

def inrange(addr):
    if int(addr,16) % 4 == 0 and int(addr,16) > 255 and int(addr,16) < 16777216:
        return True
    else:
        return False
    
def wrapper_byteget(addr):
    nhxa = int(addr, 16)
    addr = addr.upper()
    if not inrange(addr):
        return mem.getbyte(addr)
    if inrange(addr):
        print(addr)
        b1 = mem.getbyte(addr)
        b2 = mem.getbyte(str( hex ( int(addr, 16) + 1 ) )[2:].zfill(8).upper() )
        b3 = mem.getbyte(str( hex ( int(addr, 16) + 2 ) )[2:].zfill(8).upper() )
        b4 = mem.getbyte(str( hex ( int(addr, 16) + 3 ) )[2:].zfill(8).upper() )
        return str(b1+b2+b3+b4)



mapi.imgwrite('32 A = '+addr1+', 32 B = '+addr2+', 1 A = '+singl+'\n')
mem.writebyte(singl,'00')
mem.writefourbyte(addr1,'00','00','00','00')
mem.writefourbyte(addr2,'00','00','00','00')

while True:
    a = mem.getbyte(singl)
    if int(a,16) > 3:
        mapi.imgwrite(chr( int( a, 16 ) ) )
        #print(singl)
        mem.writebyte(singl,'00')
        mem.writefourbyte(addr1,'00','00','00','00')
        mem.writefourbyte(addr2,'00','00','00','00')

    if int(a,16) == 1:
        val1 = wrapper_byteget(addr1.upper())
        val2 = wrapper_byteget(addr2.upper())
        print(val1,val2)
        mem.writebyte(singl,'00')
        mem.writefourbyte(addr1,'00','00','00','00')
        mem.writefourbyte(addr2,'00','00','00','00')
        mapi.pxwrite( int(val1, 16), int(val2, 16), 3)

    if int(a,16) == 2:
        val1 = wrapper_byteget(addr1.upper())
        val2 = wrapper_byteget(addr2.upper())
        print(val1,val2)
        mem.writebyte(singl,'00')
        mem.writefourbyte(addr1,'00','00','00','00')
        mem.writefourbyte(addr2,'00','00','00','00')
        mapi.depxwrite( int(val1, 16), int(val2, 16), 3)

    if int(a,16) == 3:
        #erase whole screen
        mapi.imageblank()
        mem.writebyte(singl,'00')
        mem.writefourbyte(addr1,'00','00','00','00')
        mem.writefourbyte(addr2,'00','00','00','00')
        

    
