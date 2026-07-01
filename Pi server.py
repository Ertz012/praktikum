import socket
import struct
import requests
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
sock_send = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
sock_send.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
sock_send.bind(("192.168.1.48", 0))

port = 9999

while True:
    data, addr = sock.recvfrom(65535)
    udp_dst_port = struct.unpack("!H", data[22:24])[0]
    print("port:", udp_dst_port)
    if udp_dst_port != 9999:
        continue

    final_dst_ip = socket.inet_ntoa(data[28:32])
    print("sending to " + final_dst_ip)

    udp_payload = data[28:]
    src_ip = socket.inet_aton("192.168.1.48")
    dst_ip = socket.inet_aton(final_dst_ip)
    length = len(udp_payload)
    udp_header = struct.pack("!HHHH", 1234, port, 8 + length, 0)
    ip_header = struct.pack("!BBHHHBBH4s4s", 69, 0, 20 + 8 + length, 0, 0, 64, 17, 0, src_ip, dst_ip)

    new_packet = ip_header + udp_header + udp_payload
    sock_send.sendto(new_packet, (final_dst_ip, port))
    print("sent to " + final_dst_ip + " via wlan0")
    time.sleep(1)
    try:
        requests.post("http://192.168.1.49:5000/event", json={
            "stage": "routed",
            "final_dst": final_dst_ip,
            "src_ip": "192.168.1.101",
            "src_port": 1234,
            "dst_port": 9999,
            "checksum": int.from_bytes(data[10:12], 'big'),
            "message": udp_payload[4:].decode("utf-8", errors="ignore")
        }, timeout=1)
    except:
        pass