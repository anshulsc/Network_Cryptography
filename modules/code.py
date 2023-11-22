from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
import hashlib

# Generate a symmetric (Fernet) key
key = Fernet.generate_key()
fernet_cipher = Fernet(key)

# Message to encrypt
message = b"Your secret message here"

# Symmetric Encryption (Fernet)
encrypted_message = fernet_cipher.encrypt(message)

# Symmetric Decryption (Fernet)
decrypted_message = fernet_cipher.decrypt(encrypted_message)

# Generating RSA key pair
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

# Asymmetric Encryption (RSA)
encrypted_rsa = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Asymmetric Decryption (RSA)
decrypted_rsa = private_key.decrypt(
    encrypted_rsa,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Hashing using SHA256
hash_output = hashlib.sha256(message).hexdigest()

print("Original Message:", message.decode())
print("Symmetric Encrypted Message (Fernet):", encrypted_message)
print("Symmetric Decrypted Message (Fernet):", decrypted_message.decode())
print("Asymmetric Encrypted Message (RSA):", encrypted_rsa)
print("Asymmetric Decrypted Message (RSA):", decrypted_rsa.decode())
print("SHA256 Hash Output:", hash_output)