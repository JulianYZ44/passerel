from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

clients = []

@socketio.on('connect')
def handle_connect():
    print('Client connecté')
    clients.append(request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client déconnecté')
    clients.remove(request.sid)

@app.route('/')
def index():
    return "Serveur actif"

# Ici tu peux émettre une commande à tous les clients connectés
def send_command_to_clients(command):
    for client in clients:
        socketio.emit('command', command, to=client)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80)
