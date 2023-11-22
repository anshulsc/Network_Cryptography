import socket
import threading
import pickle
from deffh import gen_key, shared_key, decrypt , encrypt


PORT = 12391
# SERVER = socket.gethostbyname(socket.gethostname()) # Gets the IP address of the computer
SERVER = "192.168.130.202"
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

# print(SERVER)  IP address of the computer
# print(socket.gethostname()) --> Anshuls-MacBook-Air.local

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET --> IPv4, SOCK_STREAM --> TCP
server.bind(ADDR) # Binds the server to the address


g, serv_private, alpha, serv_public = gen_key(server=True)
client_public = ''
k = ''
data = ("Welcome to the server",g,alpha,serv_public)
serialized_data = pickle.dumps(data)
def handle_client(conn, addr,):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send(serialized_data) # Sends a message to the client
    data = conn.recv(1024)
    client_public = pickle.loads(data)
    k = shared_key(client_public,serv_private,g)
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) # Receives the message length
        # What is message length? --> The first message that is sent is the length of the message
        if msg_length: # If the message length is not empty
            msg_length = int(msg_length) # Converts the message length to an integer
            msg = conn.recv(msg_length).decode(FORMAT) 
            msg = decrypt(k,msg)
            if msg == DISCONNECT_MESSAGE: # If the message is the disconnect message
                connected = False
            print(f"[{addr}] Mesggage Recieved after decryption : {msg}") # Prints the message
    conn.close() 


def start():
    server.listen(5)
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept() 
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start() 
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}") 
print("Starting server...")
start() 