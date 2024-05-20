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

# github personal access token: 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