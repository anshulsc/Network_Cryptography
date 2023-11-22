import socket
import threading
import pickle
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet

sha256_hash = hashlib.sha256()


PORT = 12357
# SERVER = socket.gethostbyname(socket.gethostname()) # Gets the IP address of the computer
SERVER = "192.168.111.202"
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET --> IPv4, SOCK_STREAM --> TCP
server.bind(ADDR) # Binds the server to the address


# Generate RSA key pair for the server
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Serialize the public key for sharing with the client
public_key = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)

print("Public Key",public_key)
serialized_data = pickle.dumps(public_key)

def handle_client(conn, addr,):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send(serialized_data) # Sends a message to the client 
    digital_envelope = conn.recv(1024)
    digital_envelope = pickle.loads(digital_envelope)
    decrypted_symmetric_key = private_key.decrypt(
        digital_envelope,
        padding.OAEP(
               mgf=padding.MGF1(algorithm=hashes.SHA256()),
               algorithm=hashes.SHA256(),
               label=None,))
    cipher_suite = Fernet(decrypted_symmetric_key)
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) # Receives the message length
        print(msg_length)
        if msg_length: 
            msg_length = int(msg_length) 
            data = conn.recv(msg_length)
            data = pickle.loads(data)
            msg, dig = data
            msg = cipher_suite.decrypt(msg).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE: 
                connected = False
            if dig == hashlib.sha256(msg.encode(FORMAT)).hexdigest():
                print(f"Hash Value is same {dig}")
                print(f"[{addr}] Mesggage Recieved after decryption : {msg}")
     # Prints the message
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