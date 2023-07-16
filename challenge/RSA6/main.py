from Crypto.Util.number import long_to_bytes
import pwn

s = pwn.remote("130.192.5.212", 6646)

e = 65537
c = int(s.recvline().decode().strip())

c2e = pow(2, e) * c

print(c2e)
s.sendline(f"d{c2e}".encode())


m2 = int(s.recvline().decode().strip())
m = m2 // 2

print(long_to_bytes(m))

s.close()