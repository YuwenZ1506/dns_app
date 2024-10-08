from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

@app.route('/register', methods=['PUT'])
def register():
    data = request.json
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = data.get('as_port')

    if not all([hostname, ip, as_ip, as_port]):
        return jsonify({"HTTP Code": "400", "Error": "Missing parameters!"})

    message = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(message.encode(), (as_ip, int(as_port)))
        sock.close()
        return jsonify({"HTTP Code": "201", "Message": "Registration successful"})
    except Exception as e:
        sock.close()
        return jsonify({"Error": "Failed to send message"}), 500

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    number = request.args.get('number')
    try:
        n = int(number)
    except ValueError:
        return jsonify({"HTTP Code": "400", "Error": "Invalid number format (bad format)!"})

    def fibonacci_1(n):
        if n <= 1:
            return n
        else:
            return fibonacci_1(n-1) + fibonacci_1(n-2)
    return jsonify({"HTTP Code": "200", "Result": fibonacci_1(n)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=True)