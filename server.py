#!/usr/bin/python

from flask import Flask, jsonify, request, render_template, redirect
from flask_socketio import SocketIO
import logging, io
from PIL import Image
import base64

import ledInterface

log = logging.getLogger('werkzeug')
log.disabled = True

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
socketio = SocketIO(app)

matrix = ledInterface.MatrixManager(64, 64)

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

@socketio.on('frame')
def handle_frame(data):
    # Decode the base64 string
    image_data = base64.b64decode(data['data'])
    
    # Convert binary data to PIL image
    image = Image.open(io.BytesIO(image_data))

    matrix.set_image(data)


if __name__ == "__main__":
    print("Started Rest API")
    socketio.run(app, host="0.0.0.0", port=5000, debug=False)