import socket
import hashlib

# Server information
server_address = ("192.168.64.202", 12389)

# Create a socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

# Receive the hashed message from the server
received_hashed_message = client_socket.recv(64).decode()

# Message to verify
message = input("Enter the message to verify: ")

# Hash the message on the client side using SHA-256
sha256_hash = hashlib.sha256()
sha256_hash.update(message.encode())
client_hashed_message = sha256_hash.hexdigest()

# Verify if the received hash matches the client's hash
if received_hashed_message == client_hashed_message:
    print("Message hash matches. Message is unchanged and verified.")
else:
    print("Message hash does not match. Message may have been tampered with.")

# Close the client socket
client_socket.close()
