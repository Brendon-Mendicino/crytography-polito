from Crypto.Util.number import long_to_bytes
import pwn

s = pwn.remote("130.192.5.212", 6645)


e = 65537
n = int(s.recvline().decode().strip())
c = int(s.recvline().decode().strip())

c_inverse = pow(c, -1, n)
print(c_inverse)
s.sendline(str(c_inverse).encode())

# = c_inverse ^ d mod n
m_inverse = int(s.recvline().decode().strip())

m = pow(m_inverse, -1, n)
print(long_to_bytes(m))

s.close()