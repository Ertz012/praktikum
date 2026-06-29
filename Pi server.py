import socket
import struct
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 9999))
sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_send.bind(("192.168.1.48", 0))
port=int("9999")
while True:
    data, adress=sock.recvfrom(1024)
    checksum, length, ip_encoded = struct.unpack("!HH4s", data[0:8])
    ip_receiver = socket.inet_ntoa(ip_encoded)
    print("sending to" + ip_receiver)
    sock_send.sendto(data,(ip_receiver,port))
    print("sent to " + ip_receiver + " via wlan0")