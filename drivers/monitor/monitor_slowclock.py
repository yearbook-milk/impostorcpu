import monitor_api as mapi
import time

def fileio(name, mode, contents = ""): #file io helper
    f = open(name, mode)
    if mode == 'r':
        tr = f.read()
    if mode == 'a' or mode == 'w':
        f.write(contents)
        tr = None
    f.close()
    return tr

x = 0
y = 0
t = 3

while True:
    time.sleep(0.1)
    bus = fileio('bus1out.bus', 'r')
    bus = bus.replace(' ', '')
    #print(bus)
    if len(bus) > 2:
        print(bus[0:2])

    if bus[0:2] == '01':
        mapi.imageblank()
        print('imageblank')
    if bus[0:2] == '02':
        mapi.imagewhiteblank()
        print('imagewhite')
    if bus[0:2] == '03':
        mapi.imgwrite( chr( int(bus[2:4], 16) ) )
        print('writeASCII')
    if bus[0:2] == '04':
        mapi.deimgwrite( chr( int(bus[2:4], 16) ) )
        print('unwriteASCII')
    if bus[0:2] == '05':
        x = int(bus[4:8], 16)
        print('setx',x)
    if bus[0:2] == '06':
        y = int(bus[4:8], 16)
        print('sety',y)
    if bus[0:2] == '07':
        t = int(bus[4:8], 16)
        print('set-th')
    if bus[0:2] == '08':
        mapi.pxwrite(x,y,t)
        print('drawpx')
    if bus[0:2] == '09':
        mapi.depxwrite(x,y,t)
        print('drawpx-blank')

    f = open('bus1out.bus', 'w')
    f.close()
