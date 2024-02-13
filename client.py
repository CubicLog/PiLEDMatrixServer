import requests, io, os
from PIL import Image

#------Change Dir------
dname = os.path.dirname(os.path.realpath(__file__))
os.chdir(dname)

# Your image file
image = Image.open("EmperixLOGO64bit.png")

# Convert PIL Image to a bytes-like object that can be sent via HTTP
buf = io.BytesIO()
image.save(buf, format='JPEG')
image_bytes = buf.getvalue()

# The URL of the Flask endpoint
url = 'http://yourserveraddress/api/setimage'

# Use 'files' parameter to send image as multipart/form-data
files = {'file': ('image.jpg', image_bytes, 'image/jpeg')}

response = requests.post(url, files=files)

print(response.json())




# github personal access token: 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