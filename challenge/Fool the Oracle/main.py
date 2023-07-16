import socket
import string
from Crypto.Cipher import AES
import pwn


s = pwn.remote("130.192.5.212", 6541)

def send(array: bytes) -> bytes:
    global s
    print(s.recv(1024).decode())
    s.sendline("enc".encode())

    print(s.recv(1024).decode())
    s.sendline(array)

    output = s.recvline().decode()
    print(output)
    return bytes.fromhex(output[:-1])

flag = bytearray(b'0')

while len(flag) != 36  + len(b'CRYPTO23{}') + 1:
    data1 = bytearray(b'0' * (AES.block_size * 3 - len(flag)))
    data2 = bytearray(b'0' * (AES.block_size * 3 - len(flag)))

    for char in string.printable:
        flag[-1] = ord(char)

        to_send = data1 + flag + data2
        output = send(to_send.hex().encode())

        if output[:AES.block_size * 3] == output[AES.block_size * 3:AES.block_size * 6]:
            print(flag)
            break

        
    flag.append(0)
        
s.close()