#!/usr/bin/python

from flask import Flask, jsonify, request, render_template, redirect
from flask_socketio import SocketIO
import logging, io, os, base64
from PIL import Image
import time

import ledInterface

from threading import Thread

playing_video = False

#------Change Dir------
dname = os.path.dirname(os.path.realpath(__file__))
os.chdir(dname)

log = logging.getLogger('werkzeug')
log.disabled = True

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['UPLOAD_FOLDER'] = "uploads"
socketio = SocketIO(app)

matrix = ledInterface.MatrixManager(64, 64)

"""
def video_player(filename):
    global playing_video

    vidcap = cv2.VideoCapture(filename)
    success, image = vidcap.read()
    frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = round(vidcap.get(cv2.CAP_PROP_FPS))

    current_frame = 0
    prev_frame = -1
    deltaTime = 1
    last_time = time.time()

    while True:
        success, image = vidcap.read()
        if not success:
            break
        
        deltaTime = time.time() - last_time
        deltaTime *= fps
        last_time = time.time()

        current_frame += 1 * deltaTime

        if prev_frame != int(current_frame):
            prev_frame = int(current_frame)

            matrix.set_image(image)
    
    playing_video = False
"""
        

@app.route("/api/setimage", methods=["POST"])
def set_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        # Read the file into a bytes buffer
        file_stream = io.BytesIO(file.read())
        # Use PIL to open the image directly from the bytes buffer
        image = Image.open(file_stream)
        # Now you can process the image as needed, e.g., resize, filters, etc.
        # For demonstration, let's just print out the image size
        matrix.set_image(image)
        
        return jsonify({'message': 'Image processed successfully'}), 201

@app.route('/')
def index():
    return jsonify({}), 200

"""

@socketio.on('frame')
def handle_frame(data):
    # Decode the base64 string
    image_data = base64.b64decode(data['data'])
    
    # Convert binary data to PIL image
    image = Image.open(io.BytesIO(image_data))

    matrix.set_image(image)

@app.route('/api/uploadvideo', methods=['POST'])
def upload_video():
    global playing_video

    # Check if a video is part of the POST request
    if 'video' not in request.files:
        return jsonify({'error': 'No video part'}), 400
    video = request.files['video']
    if video.filename == '':
        return jsonify({'error': 'No selected video'}), 400
    
    if playing_video:
        return jsonify({"error": "already playing video"}), 403

    if video:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
        video.save(filename)

        Thread(target=video_player, args=[filename], daemon=True).start()

        return jsonify({'message': 'Video uploaded successfully and started playing'}), 201

"""

if __name__ == "__main__":
    print("Started Rest API")
    socketio.run(app, host="0.0.0.0", port=5000, debug=False)