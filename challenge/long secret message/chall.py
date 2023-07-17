import os, random
from Crypto.Cipher import ChaCha20
from Crypto.Util.number import long_to_bytes, bytes_to_long
from secret import flag

key = os.urandom(32)
nonce = os.urandom(12)
print(f"Using key: {key.hex()}, nonce: {nonce.hex()}")

with open("./hacker-manifesto.txt") as f:
    lines = f.readlines()

enc = []

for line in lines:
    cipher = ChaCha20.new(key=key, nonce=nonce)
    enc.append(cipher.encrypt(line.encode()).hex())

with open("./hacker-manifesto.enc", "w") as f:
    f.write("\n".join(enc))

