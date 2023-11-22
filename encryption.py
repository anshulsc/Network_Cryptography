
encrypt = lambda msg : "".join([chr(ord(x) % 128 + 3) for x in msg])
decrypt = lambda cipher :  "".join([chr(ord(x) % 128 - 3) for x in cipher])

cipher = encrypt("My name is Ansh @ 2003")

print(f'Encrypted Message : {cipher}')
print(f'Decyped Message : {decrypt(cipher)}')
