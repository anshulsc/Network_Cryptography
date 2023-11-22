import socket
import threading
import pickle
from rsa import rsa_decrypt, rsa_encrypt, rsa_gen_key

encrypt = lambda msg : "".join([chr(ord(x) % 128 + 3) for x in msg])
decrypt = lambda cipher :  "".join([chr(ord(x) % 128 - 3) for x in cipher])
PORT = 12398
# SERVER = socket.gethostbyname(socket.gethostname()) # Gets the IP address of the computer
SERVER = "172.16.177.240"
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

# print(SERVER)  IP address of the computer
# print(socket.gethostname()) --> Anshuls-MacBook-Air.local

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET --> IPv4, SOCK_STREAM --> TCP
server.bind(ADDR) # Binds the server to the address


private_key, public_key = rsa_gen_key()


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send(f"Welcome to the server!, {public_key[0]}, {public_key[1]}".encode(FORMAT)) # Sends a message to the client
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) # Receives the message length
        # What is message length? --> The first message that is sent is the length of the message
        if msg_length: # If the message length is not empty
            msg_length = int(msg_length) # Converts the message length to an integer
            msg = conn.recv(msg_length).decode(FORMAT) 
            msg = rsa_decrypt(private_key,msg)# Receives the message 
            # print(encrypt(msg[::-1]))
            # conn.send(encrypt(msg[::-1]).encode(FORMAT))
            if msg == DISCONNECT_MESSAGE: # If the message is the disconnect message
                connected = False
            print(f"[{addr}] Mesggage Recieved after decryption : {msg}") # Prints the message

        
            
    conn.close() # Closes the connection


def start():
    server.listen(5) # Listens for connections
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept() # Accepts the connection
        #conn --> socket connection of the client  #addr --> Address of the client thatconnected with the server
        thread = threading.Thread(target=handle_client, args=(conn, addr)) # Creates a thread for each client
        thread.start() # Starts the thread
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}") # Prints the number of active connections


print("Starting server...")
start() 