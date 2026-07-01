import socket
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

question = input("Default IP-Adresse benutzen? (ja/nein): ")
if question == "ja":
    ip_receiver = "192.168.1.86"
else:
    ip_receiver = input("Die Gewünschte IP-Adresse? ")

nachricht = input("Deine Nachricht? ")
data = nachricht.encode("utf-8")

src_port = 1234
dst_port = 9999
router_ip = "192.168.1.102"

src_ip = socket.inet_aton("192.168.1.101")
dst_ip = socket.inet_aton(router_ip)
final_dst = socket.inet_aton(ip_receiver)

payload = final_dst + data
length = len(payload)
checksum = sum(payload) % 65536
udp_header = struct.pack("!HHHH", src_port, dst_port, 8 + length, checksum)
ip_header = struct.pack("!BBHHHBBH4s4s", 69, 0, 20 + 8 + length, 0, 0, 64, 17, 0, src_ip, dst_ip)

packet = ip_header + udp_header + payload

try:
    sock.sendto(packet, (router_ip, dst_port))
    print("Gesendet!")
except Exception as e:
    print("Fehler:", e)