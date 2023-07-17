from Crypto.Cipher import ChaCha20
import pwn
import numpy
from string import printable, ascii_letters
import os

CHARACTER_FREQ = {
    'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610,
    'h': 0.0492888, 'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490, 'm': 0.0202124, 'n': 0.0564513,
    'o': 0.0596302, 'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357, 'u': 0.0225134,
    'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692, 'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182
} # ','

with open("./hacker-manifesto.enc", "r") as file:
    ciphertexts = []
    for line in file.readlines():
        ciphertexts.append(bytes.fromhex(line.replace("\n", "")))


print("stats")
print(len(ciphertexts))

longest_c = max(ciphertexts, key=len)
max_len = len(longest_c)
print(len(longest_c))

shortest_c = min(ciphertexts, key=len)
min_len = len(shortest_c)
print(len(shortest_c))






candidates_list = []

for byte_to_guess in range(max_len):
    freqs = numpy.zeros(256, dtype=float)

    for guessed_byte in range(256):
        for c in ciphertexts:
            if byte_to_guess >= len(c):
                continue
            if chr(c[byte_to_guess] ^ guessed_byte) in printable:
                freqs[guessed_byte] += CHARACTER_FREQ.get(chr(c[byte_to_guess] ^ guessed_byte).lower(),0)

    max_matches = max(freqs)
    # print(max_matches)

    match_list = [(freqs[i], i) for i in range(256)]
    # print(match_list)
    ordered_match_list = sorted(match_list, reverse=True)
    # print(ordered_match_list)

    # candidates = []
    # for pair in ordered_match_list:
    #     if pair[0] < max_matches * .95:
    #         break
    #     candidates.append(pair)

    # print(candidates)
    candidates_list.append(ordered_match_list)

# for c in candidates_list:
#     print(c)


keystream = bytearray()
for x in candidates_list:
    keystream += x[0][1].to_bytes(1,byteorder='big')

from Crypto.Util.strxor import strxor

def solve(row, col, ascii):
    global keystream, ciphertexts
    dec = keystream[col] ^ ciphertexts[row][col]
    mask = dec ^ ord(ascii)
    keystream[col] = keystream[col] ^ mask

solve(0, 0, 'T')
solve(0, 1, 'h')
solve(0, 2, 'i')
solve(0, 3, 's')
solve(0, 5, 'i')
solve(4, 17, 's')
solve(4, 20, 'w')
solve(0, 28, 'o')
solve(0, 38, 'e')
solve(1, 43, 'e')
solve(3, 45, 'i')
solve(3, 46, 't')
solve(0, 46, 'o')
solve(6, 45, ' ')
solve(6, 49, 'u')
solve(1, 53, 'e')
solve(1, 57, 't')
solve(1, 58, 'i')
solve(1, 59, 'n')
solve(1, 65, 'h')
solve(1, 67, 'u')
solve(6, 69, 's')


num = ""
for i in range(90):
    num += str(i // 10)
    
print(num.encode())

num = ""
for i in range(90):
    num += str(i % 10)
    
print(num.encode())

for c in ciphertexts:
    l = min(len(keystream),len(c))
    print(strxor(c[:l],keystream[:l]))

