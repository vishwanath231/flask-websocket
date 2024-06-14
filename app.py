from flask import Flask, jsonify
from flask_socketio import SocketIO, send, emit
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'seakfjgkj'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return jsonify({
        "message": "hello world!"
    })

@socketio.on('connect')
def handle_connect():
    print('Client connected!')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected!')

@socketio.on('audio')
def handle_audio(data):
    print('Received audio data')
    with open('received_recording.wav', 'wb') as f:
        f.write(data)

    audio_file_path = './beat.mp3'
    with open(audio_file_path, 'rb') as f:
        audio_data = f.read()
        emit('audio_data', {'audio': audio_data})
    # send('received audio from flutter')

@socketio.on('message')
def handle_message(message):
    print(f'Received message: {message}')
    send(message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
