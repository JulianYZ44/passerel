from flask import Flask, request, jsonify

app = Flask(__name__)

commands = {}

@app.route('/', methods=['GET', 'POST'])
def gateway():
    if request.method == 'POST':
        command = request.json.get('command')
        commands['command'] = command
        return jsonify({'status': 'success'}), 200
    return jsonify(commands), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
