import monitor_api as mapi

def fileio(name, mode, contents = ""): #file io helper
    f = open(name, mode)
    if mode == 'r':
        tr = f.read()
    if mode == 'a' or mode == 'w':
        f.write(contents)
        tr = None
    f.close()
    return tr
    
while True:
    bus = fileio('bus1out.bus', 'r')
    bus = bus.replace(' ','')
    if len(bus) > 2:
        print(bus[0:2])
    
    if bus[0:2] == '01':
        mapi.imageblank()
    if bus[0:2] == '02':
        mapi.imagewhiteblank()
    if bus[0:2] == '03':
        mapi.imgwrite( chr( int(bus[2:4], 16) ) )
    if bus[0:2] == '04':
        mapi.deimgwrite( chr( int(bus[2:4], 16) ) )
    if bus[0:2] == '05':
        x = int(bus[4:8])
    if bus[0:2] == '06':
        y = int(bus[4:8])
    if bus[0:2] == '07':
        t = int(bus[4:8])
    if bus[0:2] == '08':
        pxwrite(x,y,t)
    if bus[0:2] == '09':
        depxwrite(x,y,t)
    
    f = open('bus1out.bus', 'w')
    f.close()
