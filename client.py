import requests, io, os, time
from PIL import Image
import base64
import cv2
import socketio

import tkinter as tk
from tkinter import filedialog

#------Change Dir------
dname = os.path.dirname(os.path.realpath(__file__))
os.chdir(dname)

"""
# Your image file
image = Image.open("EmperixLOGO64bit.png")
image = image.convert("RGB")

# Convert PIL Image to a bytes-like object that can be sent via HTTP
buf = io.BytesIO()
image.save(buf, format='PNG')
image_bytes = buf.getvalue()

# The URL of the Flask endpoint

# Use 'files' parameter to send image as multipart/form-data
files = {'file': ('image.jpg', image_bytes, 'image/jpeg')}

ts = time.time()
response = requests.post('http://raspberrypi:5000/api/setimage', files=files)
te = time.time()

print(te-ts)

print(response.json())
"""

# user choose video
root = tk.Tk()
root.withdraw()
dir = filedialog.askopenfile(filetypes=[('video files','.mp4')])

# Create a Socket.IO client
sio = socketio.Client()

# Initialize Socket.IO client
sio = socketio.Client()

# Handle connection event
@sio.event
def connect():
    print("Connected to the server.")
    cap = cv2.VideoCapture(dir.name)
    i = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Resize the frame to 64x64
        resized_frame = cv2.resize(frame, (64, 64))
        
        # Convert the resized frame to JPEG and then to a base64 string
        _, buffer = cv2.imencode('.jpg', resized_frame)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')

        # Send the frame over the WebSocket connection
        sio.emit('frame', {'data': frame_base64})
        print(i)
        i += 1
        time.sleep(1/30)

    cap.release()
    sio.disconnect()

@sio.event
def disconnect():
    print("Disconnected from the server.")

# Connect to the Flask-SocketIO server
sio.connect('http://raspberrypi:5000')

# github personal access token: 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