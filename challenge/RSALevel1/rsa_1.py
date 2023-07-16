from Crypto.Util.number import bytes_to_long, getPrime
from secret import flag

p, q = getPrime(64), getPrime(64)
n = p*q
e = 65537
print(n)
m = bytes_to_long(flag)
print(pow(m,e,n))

#307138514631876566841977986823888878981
#264966476759035445244404927418681913397
