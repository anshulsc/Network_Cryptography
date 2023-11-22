import socket
import pickle
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import hashlib
from cryptography.fernet import Fernet

sha256_hash = hashlib.sha256()
key = Fernet.generate_key()
cipher_suite = Fernet(key)


PORT = 12357
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.111.202" # Gets the IP address of the computer
# SERVER = socket.gethostbyname(socket.gethostname()) # Gets the IP address of the computer
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET --> IPv4, SOCK_STREAM --> TCP
client.connect(ADDR) # Connects to the server 


def send(msg,sig):
    message = msg
    print(f'Message Sent :{message} ')
    serialized_data = pickle.dumps((message,sig))
    msg_length = len(serialized_data)  #Gets the length of the message
    send_length = str(msg_length).encode(FORMAT) # Encodes the length of the message
    send_length += b' ' * (HEADER - len(send_length)) # Adds spaces to the length of the message
    client.send(send_length)
    client.send(serialized_data) 



server_public_key = client.recv(1024)
print(server_public_key)
server_public_key = serialization.load_pem_public_key(pickle.loads(server_public_key))
digital_envelope = server_public_key.encrypt(
    key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,))

client.send(pickle.dumps(digital_envelope))


connectd = True
name = input("Enter your name: ")
while connectd:
    msg = input(f'{client.getsockname()} : {name} > ')
    sig = hashlib.sha256(msg.encode(FORMAT)).hexdigest()
    send(cipher_suite.encrypt(msg.encode(FORMAT)), sig)
    if msg == DISCONNECT_MESSAGE:
        send(DISCONNECT_MESSAGE)
        connectd = False
