from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import json
import os
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app)

# Path untuk menyimpan data chat
CHAT_HISTORY_FILE = 'chat_history.json'

# Fungsi untuk memuat riwayat chat dari file JSON
def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, 'r') as file:
            return json.load(file)
    return []

# Fungsi untuk menyimpan riwayat chat ke file JSON
def save_chat_history(history):
    with open(CHAT_HISTORY_FILE, 'w') as file:
        json.dump(history, file)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('login')
def handle_login(data):
    username = data['user']
    print(f'{username} has logged in!')

@socketio.on('chat_message')
def handle_message(data):
    print(f'Received message: {data}')
    message = data.get('msg')
    username = data.get('user')

    if message and username:
        timestamp = datetime.now().strftime('%H:%M')
        new_message = {'username': username, 'message': message, 'time': timestamp}
        
        # Load history, add new message, and save
        history = load_chat_history()
        history.append(new_message)
        save_chat_history(history)
        
        emit('receive_message', new_message, broadcast=True)

@socketio.on('request_history')
def handle_request_history():
    history = load_chat_history()
    emit('history', history)

if __name__ == '__main__':
    socketio.run(app)
