from Crypto.Util.number import long_to_bytes
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("130.192.5.212", 6647))

e = 65537
n = int(s.recv(1024))
c = int(s.recv(1024))
    
print(n)
print(c)

interval = [0, n - 1]


count = 1
while interval[0] != interval[1]:
    print(interval)

    to_send = c * pow(2, e * count, n) % n
    s.sendall((str(to_send) + "\n").encode())

    ans = int(s.recv(1024))
    
    if ans == 1:
        interval[0] = (interval[0] + interval[1]) // 2 
    else:
        interval[1] = (interval[0] + interval[1]) // 2  - 1

    count += 1


print(interval)
print(long_to_bytes(interval[0]))
