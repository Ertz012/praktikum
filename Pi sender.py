import socket
import struct
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = "192.168.1.102"
ip_receiver = "192.168.1.86"
port=int("9999")
nachricht = input("Deine Nachricht?")
data = nachricht.encode("utf-8")
ip_encode = socket.inet_aton(ip_receiver)
length = len(data)
header_length = struct.pack("!H", length)
checksum = sum(data) % 65536
header = struct.pack("!HH4s", checksum, length, ip_encode)
message = header+data
print(message)
sock.sendto(message,(ip,port))
