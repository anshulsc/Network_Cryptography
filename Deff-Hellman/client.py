import socket
import pickle
from deffh import gen_key, shared_key, decrypt , encrypt

PORT = 12391
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.130.202" # Gets the IP address of the computer
# SERVER = socket.gethostbyname(socket.gethostname()) # Gets the IP address of the computer
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET --> IPv4, SOCK_STREAM --> TCP
client.connect(ADDR) # Connects to the server 

def send(msg):
    print(f'Message Sent :{msg} ')
    message = msg.encode(FORMAT) # Encodes the message
    msg_length = len(message) # Gets the length of the message
    send_length = str(msg_length).encode(FORMAT) # Encodes the length of the message
    send_length += b' ' * (HEADER - len(send_length)) # Adds spaces to the length of the message
    client.send(send_length) # Sends the length of the message
    client.send(message) # Sends the message

recived = client.recv(1024)
data =  pickle.loads(recived)
msg,g,alpha,serv_public = data
client_private, client_public = gen_key(server=False,alpha = alpha, g = g)
k = shared_key(serv_public,client_private,g)

c_data = (client_public)
serialized_data = pickle.dumps(c_data)
client.send(serialized_data)


connectd = True
name = input("Enter your name: ")
while connectd:
    # msgserver = decrypt(client.recv(1024).decode(FORMAT))
    # print(f"Message from Serevr : {msgserver}")
    msg = input(f'{client.getsockname()} : {name} > ')
    send(encrypt(k,msg))
  
    if msg == DISCONNECT_MESSAGE:
        send(DISCONNECT_MESSAGE)
        connectd = False
