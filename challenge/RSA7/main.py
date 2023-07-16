from Crypto.Util.number import long_to_bytes
import socket
import pwn

s = pwn.remote("130.192.5.212", 6647)

e = 65537
n = int(s.recvline().decode().strip())
c = int(s.recvline().decode().strip())
    
print(n)
print(c)

interval = [0, n]


count = 1
while interval[0] != interval[1]:
    print(interval)

    to_send = c * pow(2, e * count, n) % n
    s.sendline(str(to_send).encode())

    ans = int(s.recvline().decode().strip())
    
    if ans == 1:
        interval[0] = (interval[0] + interval[1]) // 2 
    else:
        interval[1] = (interval[0] + interval[1]) // 2

    count += 1


print(interval)
print(long_to_bytes(interval[0]))
