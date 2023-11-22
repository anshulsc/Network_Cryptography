import socket
from rsa import rsa_encrypt


encrypt = lambda msg : "".join([chr(ord(x) % 128 + 3) for x in msg])
decrypt = lambda cipher :  "".join([chr(ord(x) % 128 - 3) for x in cipher])


PORT = 12398
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "172.16.177.240" 

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

msg = client.recv(2048).decode(FORMAT)
print(msg)
ls,js = msg.split(',')[1:]
public_key = (int(ls), int(js))
print(public_key)

# send(encrypt("Hello World!"))
 # Sends the message
# input() # Waits for the user to press enter

connectd = True
name = input("Enter your name: ")
while connectd:
    # msgserver = decrypt(client.recv(1024).decode(FORMAT))
    # print(f"Message from Serevr : {msgserver}")
    msg = input(f'{client.getsockname()} : {name} > ')
    send(rsa_encrypt(public_key,msg))
  
    if msg == DISCONNECT_MESSAGE:
        send(DISCONNECT_MESSAGE)
        connectd = False
