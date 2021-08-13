def fileio(name, mode, contents = ""):
    f = open(name, mode)
    if mode == 'r':
        tr = f.read()
    if mode == 'a' or mode == 'w':
        f.write(contents)
        tr = None
    f.close()
    return tr
def formats(s):
    return s.replace('0x','').replace('_', '').replace('{', '').replace('}', '').replace(' ','').replace('\n','')

file = fileio('before.txt', 'r')
instructions = file.split('\n')
endtotal = ''

for i in instructions:
    iss = i.split(' // ', 1)[0]
    cmd = iss[0:6]
    ins = iss[7:]
    tr = ''
    print(cmd+' @ '+ins)
    if cmd == 'memset':
        params = ins.split('<-')
        tr = tr + '{01 00 00} {'+formats(params[0])+'} {'+formats(params[1])+'}'
        print('01 00 MEMSET: '+tr)
    if cmd == 'memdel':
        tr = tr + '{01 01 00} {'+formats(ins)+'} {00000000}'
        print('01 01 MEMDEL: '+tr)
    if cmd == 'movmem':
        params = ins.split('->')
        tr = tr + '{00 00 00} {'+formats(params[0])+'} {'+formats(params[1])+'}'
        print('00 MOVMEM: '+tr)
    if cmd == 'stop  ':
        tr = tr + '{0D 00 00} {00 00 00 00} {00 00 00 00}'
        print('0D STOP')
    if cmd == 'remark':
        tr = ''

    if cmd == 'add   ':
        litadr = ins.split(' | ')
        params = litadr[0].split('<-')
        #print(litadr)
        if litadr[1] == 'lit':
            print('02*00 ADD: ',params[0],'+',params[1])
            tr = tr + '{02 00 00} {'+formats(params[0])+'} {'+formats(params[1])+'}'
            #print(tr)
        if litadr[1] == 'adr':
            print('02*01 ADD: ',params[0],'+',params[1])
            tr = tr + '{02 00 01} {'+formats(params[0])+'} {'+formats(params[1])+'}'
            #print(tr)

    if cmd == 'sub   ':
        litadr = ins.split(' | ')
        params = litadr[0].split('<-')
        #print(litadr)
        if litadr[1] == 'lit':
            print('03*00 SUB: ',params[0],'-',params[1])
            tr = tr + '{03 00 00} {'+formats(params[0])+'} {'+formats(params[1])+'}'
            #print(tr)
        if litadr[1] == 'adr':
            print('03*01 SUB: ',params[0],'-',params[1])
            tr = tr + '{03 00 01} {'+formats(params[0])+'} {'+formats(params[1])+'}'
            #print(tr)

    if cmd == 'mul   ':
        litadr = ins.split(' | ')
        params = litadr[0].split('<-')
        #print(litadr)
        if litadr[1] == 'lit':
            print('04*00 MUL: ',params[0],'*',params[1])
            tr = tr + '{04 00 00} {'+formats(params[0])+'} {'+formats(params[1])+'}'
            #print(tr)
        if litadr[1] == 'adr':
            print('04*01 MUL: ',params[0],'*',params[1])
            tr = tr + '{04 00 01} {'+formats(params[0])+'} {'+formats(params[1])+'}'
            #print(tr)

    if cmd == 'div   ':
        litadr = ins.split(' | ')
        params = litadr[0].split('<-')
        #print(litadr)
        if litadr[1] == 'lit':
            print('05*00 DIV: ',params[0],'/',params[1])
            tr = tr + '{05 00 00} {'+formats(params[0])+'} {'+formats(params[1])+'}'
            #print(tr)
        if litadr[1] == 'adr':
            print('05*01 DIV: ',params[0],'/',params[1])
            tr = tr + '{05 00 01} {'+formats(params[0])+'} {'+formats(params[1])+'}'
            #print(tr)

    if cmd == 'label ':
        tr = tr + '{06 00 00} {'+formats(ins)+'} {00 00 00 00}'
        print('06 LABEL')

    if cmd == 'goto  ':
        litadr = ins.split(' | ')
        if litadr[1] == 'lit':
            tr = tr + '{0C} {' + formats(litadr[0]) + '} {00 00 00 00 00 00}'
            print('0C GOTO:',litadr[0])
        if litadr[1] == 'adr':
            tr = tr + '{07} {'+formats(litadr[0])+'} {00 00 00 00 00 00}'
            print('07 GOTO:',litadr[0])
            print(tr)

    if cmd == 'compar':
        operators = {
'>=': '00',
'>': '01',
'<=': '02',
'<': '03',
'==': '04',
'!=': '05',
            }
        toplevel = ins.split(' | ')
        midlevel = toplevel[0].split(' ')
        #print(midlevel)
        litadr1 = midlevel[0][0:3]
        litadr2 = midlevel[2][0:3]
        #print(litadr1,litadr2)

        if litadr1=='lit' and litadr2=='lit':
            litadrfinal = '00'
        if litadr1=='lit' and litadr2=='adr':
            litadrfinal = '01'
        if litadr1=='adr' and litadr2=='lit':
            litadrfinal = '02'
        if litadr1=='adr' and litadr2=='adr':
            litadrfinal = '03'
        
        tr = tr + '{08} {'+litadrfinal+'} {'+formats(midlevel[0][4:-1])+'} {'+operators[midlevel[1]]+'} {'+formats(midlevel[2][4:-1])+'}'
        print('08',litadrfinal,'COMPAR:',tr)

        if len(toplevel) > 1:
            tr = tr + '\n{00 00 00} {00 00 00 01} {'+formats(toplevel[1])+'}'
            print('MOVMEM flag, to',toplevel[1])
            
        
    endtotal = endtotal + tr + '\n'
    print('\n')

fileio('after.txt','w',endtotal)
