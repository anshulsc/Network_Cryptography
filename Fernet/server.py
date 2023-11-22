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


PORT = 12329
SERVER = "192.168.105.202"
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
server_public_key = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)


serialized_data = pickle.dumps(server_public_key)

def verify_digital_signature(message, signature, public_key):
    hashed_message = hashlib.sha256(message.encode(FORMAT)).digest()
    try:
        public_key.verify(
            signature,
            hashed_message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        print(e)
        return False
    

def handle_client(conn, addr,):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send(serialized_data) # Sends server public key to client 
    
    # Getting client public key
    client_public_key  = conn.recv(1024)
    client_public_key = serialization.load_pem_public_key(pickle.loads(client_public_key))
    
    # Getting Symmetric Key
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
        if msg_length: 
            msg_length = int(msg_length)
            
            # Get pickle data containing message and dig_sig
            data = conn.recv(msg_length)
            data = pickle.loads(data)
            
            msg, dig_sig = data
            msg = cipher_suite.decrypt(msg).decode(FORMAT)
            
            if msg == DISCONNECT_MESSAGE: 
                connected = False
            
            if verify_digital_signature(msg, dig_sig, client_public_key):
                print(f"[{addr}] Mesggage Recieved after decryption : {msg}")
                
    conn.close() 


def start():
    server.listen(30)
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept() 
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start() 
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}") 
print("Starting server...")

start() 