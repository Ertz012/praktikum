import socket
import requests

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 9999))

while True:
    data, addr = sock.recvfrom(1024)
    message = data[4:].decode("utf-8")
    print("Nachricht:", message)
    try:
        requests.post("http://192.168.1.49:5000/event", json={
            "stage": "routed",
            "final_dst": final_dst_ip
        }, timeout=1)
    except:
        pass