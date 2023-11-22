from socket import *
import socket
import sys

# 创建 socket
try:
    tcpSerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
    print(msg)
    sys.exit()

print("Socket created")

target_host = input("Enter a host to connect to: ")
target_port = int(input("Enter a port to connect to: "))



 # 90 perecent of the time, you don't need to specify the port number,
 # it will be assigned automatically
 # Socket family is AF_INET, socket type is SOCK_STREAM
    # AF_INET means that the underlying network is using IPv4
    # SOCK_STREAM means that the underlying network is using TCP

try:
    tcpSerSocket.connect((target_host,target_port))
    print(f'Socket connected to {target_host} on port {target_port}')
    tcpSerSocket.shutdown(2)
except socket.error as msg:
    print(f'Failed to connect to {target_host} on port {target_port}')
    print(msg)
    sys.exit()
