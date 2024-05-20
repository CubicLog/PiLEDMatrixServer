import cv2
import base64
import websocket
import json
from PIL import Image
import io

# Function to convert a frame to base64
def frame_to_base64(frame):
    pil_im = Image.fromarray(frame)
    buff = io.BytesIO()
    pil_im.save(buff, format="JPEG")
    img_str = base64.b64encode(buff.getvalue()).decode("utf-8")
    return img_str

# Callback function when the websocket is opened
def on_open(ws):
    print("WebSocket opened")
    cap = cv2.VideoCapture('bad apple.mp4')
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("break")
            break
        
        # Convert frame to base64
        img_str = frame_to_base64(frame)
        
        # Send frame via websocket
        ws.send(json.dumps({"data": img_str}))

    print("close")
    cap.release()
    ws.close()

# Callback function when a message is received
def on_message(ws, message):
    print(f"Received: {message}")

# Callback function when an error occurs
def on_error(ws, error):
    print(f"Error: {error}")

# Callback function when the websocket is closed
def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed")

if __name__ == "__main__":
    ws = websocket.WebSocketApp("ws://raspberrypi:5000",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()