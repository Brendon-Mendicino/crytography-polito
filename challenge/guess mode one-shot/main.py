import socket
import pwn

s = pwn.remote("130.192.5.212", 6531)

for i in range(128):
    # challenge
    print(s.recvline().decode())

    otp = s.recvline().decode()
    print(otp)
    otp = otp.removeprefix("The otp I'm using: ").strip()
    otp = bytes.fromhex(otp)

    data = bytes.fromhex("aa" * 32)
    data = bytes([d ^ o for d,o in zip(data,otp)])

    print(s.recv().decode())
    s.sendline(data.hex().encode())

    output = s.recvline().decode()
    print(output)
    output = bytes.fromhex(output.removeprefix("Output: ").strip())

    print(s.recvline().decode())
    if output[:16] == output[16:32]:
        print("ECB")
        s.sendline("ECB".encode())
    else:
        print("CBC")
        s.sendline("CBC".encode())

    print(s.recvline().decode())

print(s.recvline().decode())

s.close()