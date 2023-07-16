import socket
import pwn

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("130.192.5.212", 6531))

for i in range(128):
    # challenge
    otp = s.recv(4096).decode()
    print("CHALLANGE: " + otp)

    otp = otp.splitlines() if otp.splitlines()[0].find("OK, next") == -1 else otp.splitlines()[1:]
    otp = otp[1].removeprefix("The otp I'm using: ")[:64]
    otp = bytes.fromhex(otp)

    data = bytes.fromhex("aa" * 32)
    data = bytes([d ^ o for d,o in zip(data,otp)])

    if i == 0:
        print("INPUT: " + s.recv(4096).decode())
    s.sendall(f"{data.hex()}\n".encode())

    output = s.recv(4096).decode()
    print("OUTPUT: " +  output)
    output = bytes.fromhex(output.removeprefix("Output: ")[:64])

    if output[:16] == output[16:32]:
        print("ECB")
        s.sendall("ECB\n".encode())
    else:
        print("CBC")
        s.sendall("CBC\n".encode())

    print("NEXT: " + s.recv(4096).decode())

print(s.recv(4096).decode())