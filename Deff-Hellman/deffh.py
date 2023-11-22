import math
import random


def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def gen_prime_num(server = False):
    p,q = 0,0
    while True:
        p = random.randint(100, 500)
        if is_prime(p):
            break
    if not server:
        return p
    else:
        while True:
            q = random.randint(100, 500)
            if is_prime(q) and q != p:
                break
    return p, q

def find_primitive_root(p):
    if not is_prime(p):
        raise ValueError("Input is not a prime number")

    for g in range(2, p):
        if all(pow(g, k, p) != 1 for k in range(1, p - 1)):
            return g

    raise ValueError(f"No primitive root found for {p}")


def gen_key(server=False, alpha = 0, g=0):
    if server:
        g, private_key = gen_prime_num(server)
        alpha = find_primitive_root(g)
        public_key =  pow(alpha,private_key,g)
        return g,private_key,alpha,public_key
    else:
        private_key = gen_prime_num(server)
        public_key =  pow(alpha,private_key,g)
        return private_key,public_key


def shared_key(public_key , private_key, g):
    return pow(public_key, private_key,g)

def encrypt(k,plaintext):
    return "".join([chr(ord(x) + k ) for x in plaintext])

def decrypt(k,plaintext):
    return "".join([chr(ord(x) - k) for x in plaintext])


g, serv_private, alpha, serv_public = gen_key(server = True)
client_private, client_public = gen_key(server=False, alpha = alpha, g = g)

if __name__ == '__main__':
    client_side = shared_key(serv_public,client_private,g)
    serv_side  = shared_key(client_public,serv_private,g)

    print(f'Client Side Shared Key: {client_side}')
    print(f'Sever Side Shared key: {serv_side}')

    msg = "hi there!"
    print(f'Encrypted Message : {encrypt(serv_side,msg)}')
    print(f'Decrypted Message : {decrypt(client_side,encrypt(serv_side,msg))}')
