from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

COMMAND_FILE = 'commands.json'

def init_command_file():
    if not os.path.exists(COMMAND_FILE):
        with open(COMMAND_FILE, 'w') as f:
            json.dump({'launch': False}, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/launch', methods=['POST'])
def launch():
    with open(COMMAND_FILE, 'w') as f:
        json.dump({'launch': True}, f)
    return jsonify({'status': 'Launched'})

@app.route('/status')
def status():
    with open(COMMAND_FILE) as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/reset', methods=['POST'])
def reset():
    with open(COMMAND_FILE, 'w') as f:
        json.dump({'launch': False}, f)
    return jsonify({'status': 'Reset'})

if __name__ == '__main__':
    init_command_file()
    app.run(host='0.0.0.0', port=10000)
