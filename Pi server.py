import socket
import struct
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('192.168.1.102', 9999))
port=int("9999")
while True:
    data, adress=sock.recvfrom(1024)
    checksum, length, ip_encoded = struct.unpack("!HH4s", data[0:8])
    ip_receiver = socket.inet_ntoa(ip_encoded)
    print("sending to" + ip_receiver)
    sock.sendto(data,(ip_receiver,port))