import socket
import json
import threading

dns_records = {}

def handle_registration(data):
    lines = data.strip().split('\n')
    hostname = None
    ip_address = None
    
    for line in lines:
        if line.startswith("NAME="):
            hostname = line.split('=')[1].strip()
        elif line.startswith("VALUE="):
            ip_address = line.split('=')[1].strip()

    if hostname and ip_address:
        dns_records[hostname] = ip_address # Store the ip address of FS
        with open('dns_records.json', 'w') as f:
            json.dump(dns_records, f)
        return "Registration Successful"
    else:
        return "Invalid Registration data"


def handle_query(data):
    lines = data.split('\n')
    hostname = lines[1].split('=')[1].strip()
    ip_address = dns_records.get(hostname, None)
    if ip_address:
        response = f"TYPE=A\nNAME={hostname}\nVALUE={ip_address}\nTTL=10\n"
    else:
        response = "Record not found"
    return response

def udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 53533))
    while True:
        data, addr = sock.recvfrom(1024)
        lines = data.decode().strip().split('\n')

        # Deal with request from FS
        if len(lines) >= 3 and "TYPE=" in lines[0] and "VALUE=" in lines[2]:
            response = handle_registration(data.decode())
        # Deal with request from US
        elif len(lines) >= 2 and "TYPE=" in lines[0] and "VALUE=" not in lines[1]:
            response = handle_query(data.decode())
        else:
            response = "Invalid request format"
        sock.sendto(response.encode(), addr)

if __name__ == '__main__':
    try:
        with open('dns_records.json', 'r') as f:
            dns_records = json.load(f)
    except FileNotFoundError:
        print("No existing DNS records found, starting with an empty registry.")
    
    threading.Thread(target=udp_server).start()
