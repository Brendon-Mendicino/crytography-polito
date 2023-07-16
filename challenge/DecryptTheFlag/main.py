import random
import pwn
import string

s = pwn.remote("130.192.5.212", 6561)


def next(array: bytes) -> str:
    print(s.recv().decode())
    s.sendline("y".encode())

    print(s.recv().decode())
    s.sendline(array)

    output = s.recvline().decode().strip()
    print(output)
    return output
    

print(s.recvline().decode())
seed = 0
s.sendline(str(seed).encode())

print(s.recvline().decode())

c1 = s.recvline().decode()
print(c1)
c1 = bytes.fromhex(c1)

# build keystream
keystream_xor = bytes.fromhex(next(("0" * 60).encode()))
keystream = bytearray()
for byte in keystream_xor:
    keystream.append(byte ^ ord('0'))

keylen = len(c1) // 2
flag = bytearray([0])

for index, byte in enumerate(c1):
    for char in string.printable:

        if ord(char) ^ byte == keystream[index]:
            flag[-1] = ord(char)
            print(flag)
            break

    flag.append(0)


s.close()