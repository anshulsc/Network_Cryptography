import socket
import pickle
from cryptography.fernet import Fernet

PORT = 12399

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




recived = client.recv(1024)
data =  pickle.loads(recived)
msg,key = data
print(key)
cipher_suite = Fernet(key)


connectd = True
name = input("Enter your name: ")
while connectd:
    # msgserver = decrypt(client.recv(1024).decode(FORMAT))
    # print(f"Message from Serevr : {msgserver}")
    msg = input(f'{client.getsockname()} : {name} > ')
    send(cipher_suite.encrypt(msg.encode(FORMAT)))
  
    if msg == DISCONNECT_MESSAGE:
        send(DISCONNECT_MESSAGE)
        connectd = False
