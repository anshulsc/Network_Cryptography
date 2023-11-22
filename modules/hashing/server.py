import socket
import hashlib

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind( ("192.168.64.202", 12389))
server_socket.listen(1)

print("Server is listening...")

# Accept a connection from a client
client_socket, addr = server_socket.accept()
print(f"Connected to {addr}")

# Message to send
message = "Anshul Singh"

# Hash the message using SHA-256
sha256_hash = hashlib.sha256()
sha256_hash.update(message.encode())
hashed_message = sha256_hash.hexdigest()

# Send the hashed message to the client
client_socket.send(hashed_message.encode())

# Close the sockets
client_socket.close()
server_socket.close()
