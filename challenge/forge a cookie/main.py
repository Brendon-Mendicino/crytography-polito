import socket
import base64

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("130.192.5.212", 6521))

print(s.recv(1024).decode())

name = "brebrebrebrebreb"
input_msg = name

s.sendall(f"{input_msg}\n".encode())


print(s.recv(1024).decode())
token = s.recv(1024).decode()
print(token)
token = token.removeprefix("This is your token: ").split(".")
nonce = base64.b64decode(token[0])
enc_token = base64.b64decode(token[1])

s.sendall("flag\n".encode())

print(s.recv(1024).decode())

#{"username":"bre"}
token_string = b'{"username": "brebrebrebrebreb"}'
new_string   = b'{"username": "b", "admin": true}'
enc_token = bytearray(enc_token)
for (i, (b, n)) in enumerate(zip(token_string, new_string)):
    enc_token[i] ^= b ^ n

new_token = f"{base64.b64encode(nonce).decode()}.{base64.b64encode(enc_token).decode()}"
print(new_token)
s.sendall(f"{new_token}\n".encode())

print(s.recv(1024).decode())