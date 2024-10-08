from flask import Flask, request, jsonify
import requests
import socket

app = Flask(__name__)

def get_ip_from_as(hostname, as_ip, as_port):
    message = f"TYPE=A\nNAME={hostname}\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (as_ip, int(as_port)))
    response, _ = sock.recvfrom(1024)
    sock.close()
    return response.decode().split('\n')[2].split('=')[1]

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    if not all([hostname, fs_port, number, as_ip, as_port]):
        return jsonify({"HTTP Code": "400", "Error": "Missing parameters! Bad request!"})
      
    try:
        ip_address = get_ip_from_as(hostname, as_ip, as_port)
    except Exception as e:
        return jsonify({"Error": str(e)}), 500

    try:
        response = requests.get(f"http://{ip_address}:{fs_port}/fibonacci?number={number}")
        return response.content, response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"Error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)