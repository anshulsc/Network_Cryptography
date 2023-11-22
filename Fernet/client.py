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


PORT = 12329
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.105.202" 
ADDR = (SERVER, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg,sig):
    message = msg
    print(f'Message Sent :{message} ')
    serialized_data = pickle.dumps((message,sig))
    msg_length = len(serialized_data)  #Gets the length of the message
    send_length = str(msg_length).encode(FORMAT) # Encodes the length of the message
    send_length += b' ' * (HEADER - len(send_length)) # Adds spaces to the length of the message
    client.send(send_length)
    client.send(serialized_data) 


# Recieving Server Public Key
server_public_key = client.recv(1024)
print(server_public_key)
server_public_key = serialization.load_pem_public_key(pickle.loads(server_public_key))




# Generate RSA key pair for the server
client_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
# Serialize the public key for sharing with the client
client_public_key = client_private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)
serialized_data = pickle.dumps(client_public_key)
client.send(serialized_data) # Sharing client public key


# Sharing symmetric key as digital envelope
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
    hashed_message = hashlib.sha256(msg.encode(FORMAT)).digest()
    signature = client_private_key.sign(
        hashed_message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    send(cipher_suite.encrypt(msg.encode(FORMAT)), signature)
    if msg == DISCONNECT_MESSAGE:
        send(DISCONNECT_MESSAGE)
        connectd = False
