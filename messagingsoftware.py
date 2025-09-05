'''
Hello sagar bhai this is the code for messaging back and forth real time..
i have used many comments in this code so as it can be easy to understand.. 
i have corrected many mistakes in this code with the help of chatgpt and youtube.. 
i have also uploaded the raw/older code having some mistakes.. 
sorry i was unable to include end to end encryption(e2ee) in this code..
because i was facing a problem in vs code..
i had installed cryptography and also made a fernet key for e2ee..
still i was trying to resolve that problem for the last 2 hours but it is not resolved 
'''


import socket   #socket for networking
import threading   #threading to keep UI responsive while sending/receiving messages
from tkinter import *   #socket for networking


# this script combines both sender and receiver functionalities into one script, so that a single app can:
    # start a server socket to listen for incoming messages.
    # connect to another chat client as a client socket to send messages.
    # show everything in a graphical window using Tkinter.


# --- GUI Setup ---

# GUI Setup (Tkinter)
make = Tk()  #creates the main window (make)
make.geometry("400x600")  #sets window size to 400x600 pixels
make.config(bg="white")   #background color is white
make.title("Chat App (Sender + Receiver)")  #title will be shown in the window bar

# Message input handling
message = StringVar()  # StringVar used here to track what the user types in the message box.

# Message display (Chat history)
lstbox = Listbox(make, height=20, width=43)  # listbox widget is used to display incoming and outgoing messages.
lstbox.place(x=15, y=80)  # placed at position (15, 80) in the window.

# Text input box
messagebox = Entry(make, textvariable=message, font=('calibre', 12, 'normal'), border=2, width=32) # Entry widget lets the user type a message. It uses the message variable to store what’s typed.
messagebox.place(x=10, y=444)  # placed at (10, 444) near the bottom.


# --- Networking Variables ---

receiver_port = 3050  # port on which server will listen on
sender_socket = None  # client socket for sending messages. will be created on connect
connection_socket = None  # socket that represents the incoming connection (used for receiving). used to receive messages


# --- Receive Messages (Server) ---

def start_server(): 
    def recv():
        global connection_socket
        server_socket = socket.socket()   # sets up a server socket.
        server_socket.bind(('', receiver_port))  # bind() tells it to listen on all IPs ('') and the port 3050
        server_socket.listen(1)   # listen() starts listening
        print("Server listening on port", receiver_port)
        connection_socket, addr = server_socket.accept()   # accept() waits for a client to connect.
        print("Connected by", addr)  
        lstbox.insert(0, f"Connected to {addr}")    # once connected, it stores the connection in connection_socket
        
        # Receiving messages continuously
        # enters a loop to receive messages
        while True:
            try:
                data = connection_socket.recv(1024).decode()   # recv(1024) reads up to 1024 bytes. decode() converts bytes to string
                if data:
                    lstbox.insert(0, "Friend: " + data)   # if a message is received, it is shown in the chat window (lstbox)
            except:
                break
    
    # Run server in a thread
    t = threading.Thread(target=recv)   # starts the recv function in a separate thread, so it doesn't freeze the GUI
    t.daemon = True
    t.start()

# --- Send Messages (Client) ---
def connect_to_friend():
    global sender_socket
    friend_ip = ip_entry.get()  # retrieves the IP and port of the friend from the text inputs
    friend_port = int(port_entry.get())
    sender_socket = socket.socket()   # Creates a new client socket

    try:   # tries to connect to the friend's server socket
        sender_socket.connect((friend_ip, friend_port))   
        lstbox.insert(0, f"Connected to friend at {friend_ip}:{friend_port}")   # if successful, adds a message to the chat window
    except Exception as e:
        lstbox.insert(0, f"Connection failed: {e}")   # If failed, shows an error message

# Sending Messages
def send_msg():
    msg = message.get()   # gets the typed message
    if msg and sender_socket:
        try:
            sender_socket.send(msg.encode())   # sends it using the sender_socket
            lstbox.insert(0, "You: " + msg)    # shows it in the chat window
        except:
            lstbox.insert(0, "Failed to send message.")   # handles any error if the message can't be sent

# Threaded send function
def thread_send_msg():
    threading.Thread(target=send_msg).start()   # runs the send_msg() function in a new thread to keep the GUI responsive


# --- GUI Buttons and Inputs ---

# start server Button
Button(make, text="Start Server", command=start_server).place(x=10, y=10)   # button to start the receiver (server socket)

# friend IP and port entry
Label(make, text="Friend IP:").place(x=10, y=40)   # lets the user input the friend's IP address
ip_entry = Entry(make, width=20)
ip_entry.place(x=80, y=40)
ip_entry.insert(0, 'localhost')  # Default value for local testing

Label(make, text="Port:").place(x=10, y=65)   # lets the user input the port the friend's app is listening on
port_entry = Entry(make, width=10)
port_entry.place(x=80, y=65)
port_entry.insert(0, '3050')  # Default port

# connect to friend button
Button(make, text="Connect to Friend", command=connect_to_friend).place(x=200, y=50)   # when clicked, connects to the friend's server using the provided IP and port

# send message button
Button(make, text="Send", command=thread_send_msg).place(x=260, y=440)   # sends the message when clicked, using a new thread

# finally, start the GUI event loop
make.mainloop()   # this keeps the window open and waits for user actions (clicks, typing, etc.)


'''
HOW TO USE

On App 1:
Click Start Server
Leave the IP as localhost
Click Connect to Friend

On App 2:
Click Start Server
In the IP box, type localhost or the IP of App 1's machine
Click Connect to Friend
'''


