from flask import Flask, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/event", methods=["POST"])
def event():
    data = request.get_json()
    socketio.emit("packet_event", data)
    return jsonify({"status": "ok"})

@app.route("/")
def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
