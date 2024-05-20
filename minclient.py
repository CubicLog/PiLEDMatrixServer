import websocket
import json
import base64
from PIL import Image
import io

websocket.enableTrace(True)

def on_open(ws):
    print("WebSocket opened")
    # Create a simple image for testing
    image = Image.new('RGB', (100, 100), color=(73, 109, 137))
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    test_data = {"data": img_str}
    ws.send(json.dumps(test_data))

def on_message(ws, message):
    print(f"Received message: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed")

if __name__ == "__main__":
    ws = websocket.WebSocketApp("ws://localhost:5000",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()