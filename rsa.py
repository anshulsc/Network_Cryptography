import random
import math

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True



def gen_prime_num():
    p,q = 0,0
    while True:
        p = random.randint(100, 500)
        if is_prime(p):
            break

    while True:
        q = random.randint(100, 500)
        if is_prime(q) and q != p:
            break
    return p,q

def mod_inverse(a, m):
    x0, x1, m0 = 0, 1, m
    
    while a > 1:
        q = a // m
        m, a = a % m, m
        x_temp = x1 - q * x0
        x1, x0 = x0, x_temp
    
    return x1 + m0 if x1 < 0 else x1

def rsa_gen_key(random_prime= False):
    if random_prime:
        p,q = gen_prime_num()
    else:
        p,q = 113, 307

    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = random.randint(2, phi_n - 1)
    while math.gcd(e, phi_n) != 1:
        e = random.randint(2, phi_n - 1)

    d = mod_inverse(e, phi_n)
    return (n, d), (n, e)

private_key, public_key = rsa_gen_key()
print(private_key)

def rsa_encrypt(public_key, plaintext):

    n, e = public_key[0], public_key[1]

    encrypt = lambda text : ''.join([chr((ord(x)**e)%n) for x in text])
    encrypted = encrypt(plaintext)

    return encrypted


def rsa_decrypt(private_key, ciphertext):
    n, d =  private_key[0], private_key[1]

    decrypt = lambda text : ''.join([chr((ord(x)**d)%n) for x in text])
    decrypted = decrypt(ciphertext)

    return decrypted

if __name__ == "__main__" :
    cipher = rsa_encrypt(public_key,"hi my name is ")
    print(cipher)
    print(rsa_decrypt(private_key,cipher))
