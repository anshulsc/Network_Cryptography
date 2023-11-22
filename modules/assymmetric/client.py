import socket
import pickle

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import hashlib

PORT = 12373
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.64.202" # Gets the IP address of the computer
# SERVER = socket.gethostbyname(socket.gethostname()) # Gets the IP address of the computer
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET --> IPv4, SOCK_STREAM --> TCP
client.connect(ADDR) # Connects to the server 

def send(msg):
    print(f'Message Sent :{msg} ')
    message = msg
    msg_length = len(message) # Gets the length of the message
    send_length = str(msg_length).encode(FORMAT) # Encodes the length of the message
    send_length += b' ' * (HEADER - len(send_length)) # Adds spaces to the length of the message
    client.send(send_length) # Sends the length of the message
    client.send(message) # Sends the message

server_public_key = client.recv(1024)
print(server_public_key)
server_public_key = serialization.load_pem_public_key(pickle.loads(server_public_key))



connectd = True
name = input("Enter your name: ")
while connectd:
    # msgserver = decrypt(client.recv(1024).decode(FORMAT))
    # print(f"Message from Serevr : {msgserver}")
    msg = input(f'{client.getsockname()} : {name} > ')
    send(server_public_key.encrypt(
    msg.encode(FORMAT),
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )
))
  
    if msg == DISCONNECT_MESSAGE:
        send(DISCONNECT_MESSAGE)
        connectd = False
