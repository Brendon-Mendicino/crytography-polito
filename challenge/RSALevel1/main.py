from Crypto.Util.number import long_to_bytes
n = 307138514631876566841977986823888878981

# c = pow(m, e, n)  => m = ?, m = pow(c, d, n)
c = 264966476759035445244404927418681913397

p = 16785115384266113939
q = 18298266505798310279

e = 65537
d = pow(e, -1, (p - 1) * (q - 1))
m = pow(c, d, n)
print(m)


print(long_to_bytes(m))