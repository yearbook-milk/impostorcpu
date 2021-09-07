import tkinter as tk

def fileio(name, mode, contents = ""): #file io helper
    f = open(name, mode)
    if mode == 'r':
        tr = f.read()
    if mode == 'a' or mode == 'w':
        f.write(contents)
        tr = None
    f.close()
    return tr
    
def callbackfunc(key):
    print(chr( int(key,16) ))
    fileio('bus1in.bus', 'w', '00 00 00 '+str(key))

buttons = []

root = tk.Tk()
buttons.append(tk.Button(text='1 DOWN    ', command=lambda: callbackfunc('31')))
buttons.append(tk.Button(text='2 UP    ', command=lambda: callbackfunc('32')))
buttons.append(tk.Button(text='3 LEFT  ', command=lambda: callbackfunc('33')))
buttons.append(tk.Button(text='4 RIGHT ', command=lambda: callbackfunc('34')))
buttons.append(tk.Button(text='5 ENTER ', command=lambda: callbackfunc('35')))
buttons.append(tk.Button(text='6 CANCEL', command=lambda: callbackfunc('36')))
buttons.append(tk.Button(text='7 PEN UP', command=lambda: callbackfunc('37')))
buttons.append(tk.Button(text='8 PEN DN', command=lambda: callbackfunc('38')))
buttons.append(tk.Button(text='9       ', command=lambda: callbackfunc('39')))
buttons.append(tk.Button(text='0       ', command=lambda: callbackfunc('30')))

for i in buttons:
    i.pack()
    
root.mainloop()
