
from Crypto.Util.number import long_to_bytes

n = 1002377325462265193999966239331938420043855910747382013931673
e = 3
ct = 3239652861114474176617817642126683102816200405503678601991



# factorDB

p = 934637197090526256706525222709
q = 1072477458186567150192511962197

phi = (q - 1)*(p - 1)
d = pow(e, -1, phi)

m = pow(ct, d, n)
print(long_to_bytes(m))