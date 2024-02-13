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

# Open the input video
cap = cv2.VideoCapture(dir.name)
# Get video codec and fps
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Adjust codec as per your video format
fps = cap.get(cv2.CAP_PROP_FPS)

new_path = f"{dir.name.split(".")[0]} [RESIZED64x64]{dir.name.split(".")[1]}"

# Create a VideoWriter object for the output video
out = cv2.VideoWriter(new_path, fourcc, fps, (64, 64))

print("resizing...")
# Read and resize each frame
while True:
    ret, frame = cap.read()
    if not ret:
        break
    resized_frame = cv2.resize(frame, (64, 64))
    out.write(resized_frame)

print("finished resizing")

# Release everything
cap.release()
out.release()

# Upload the resized video to the server
url = 'http://raspberrypi:5000/api/uploadvideo'
files = {'video': open(new_path, 'rb')}
response = requests.post(url, files=files)

print("uploaded")

# github personal access token: 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