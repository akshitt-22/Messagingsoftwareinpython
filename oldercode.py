import socket 
import time 
import threading 
from tkinter import * 

make = Tk() 
make.geometry("400×600") 
make.config(bg="white") 

def func(): 
    t= threading.Thread(target=recv) 
    t.start() 
    
def recv(): 
    listensocket = socket.socket() 
    port = 3050 
    maxconnection=99 
    ip=socket.gethostname() 
    print(ip) 
    
    listensocket.bind(('',port)) 
    listensocket.listen(maxconnection) 
    (clientsocket, address) = listensocket.accept() 
    
    while True: 
        sendermessage = clientsocket.recv(1024).decode() 
        if not sendermessage=="": 
            time.sleep(5) 
            lstbox.insert(0, "Client: "+sendermessage) 
            
            
xr = 0 

def sendmsg(): 
    global xr 
    if xr == 0: 
        s = socket.socket() 
        hostname = 'LAPTOP-7CVTO876' 
        port = 4050 
        s.connect((hostname, port)) 
        msg = messagebox.get() 
        lstbox.insert(0, "You : "+ msg) 
        s.send(msg.encode()) 
        xr = xr+1 
        
    else: 
        msg = messagebox.get() 
        lstbox.insert(0, "You :"+ msg) 
        s.send(msg.encode()) 
        
def threadsendmsg(): 
    th = threading.Thread(target=sendmsg) 
    th.start() 
    
startimage = PhotoImage(file = "start.png") 

buttons = Button(make, image=startimage, command=func, borderwidth=0) 
buttons.place(x=90, y=10) 

message = StringVar() 
messagebox = Entry(make, textvariable = message, font =('calibre',12,'normal'), border = 2, width = 32) 
messagebox.place(x=10, y=444) 

sendmessageimg = PhotoImage(file='send.png') 
sendmessagebutton = Button(make, image=sendmessageimg, command = threadsendmsg, borderwidth=0) 
sendmessagebutton.place(x=260, y=440) 

lstbox = Listbox(make, height=20, width=43) 
lstbox.place(x=15, y=80) 

make.mainloop()