import socket
import threading
import pickle
from cryptography.fernet import Fernet


PORT = 12399
# SERVER = socket.gethostbyname(socket.gethostname()) # Gets the IP address of the computer
SERVER = "192.168.64.202"
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

# print(SERVER)  IP address of the computer
# print(socket.gethostname()) --> Anshuls-MacBook-Air.local

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET --> IPv4, SOCK_STREAM --> TCP
server.bind(ADDR) # Binds the server to the address

key = Fernet.generate_key()

# Data to send to client
data = ("Welcome to the server",key)
serialized_data = pickle.dumps(data)

cipher_suite = Fernet(key)




def handle_client(conn, addr,):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send(serialized_data) # Sends a message to the client
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) # Receives the message length
        # What is message length? --> The first message that is sent is the length of the message
        if msg_length: 
            msg_length = int(msg_length) 
            msg = conn.recv(msg_length)
            msg = cipher_suite.decrypt(msg).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE: 
                connected = False
            print(f"[{addr[1]}] :: Mesggage Recieved after decryption : {msg}") # Prints the message
    conn.close() 


def start():
    server.listen(5)
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept() 
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start() 
        print("-------------------------------------------")
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}") 

print("Starting server...")
start() 