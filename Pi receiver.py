import socket
import struct
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('192.168.1.86', 9999))
while True:
    data, adress=sock.recvfrom(1024)
    checksum, length, ip_receiver = struct.unpack("!HH4s", data[0:8])
    print(data[8:].decode("utf-8"))