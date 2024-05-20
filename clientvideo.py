import cv2
import base64
import websocket
import json
from PIL import Image
import io

import asyncio
import websockets
import time

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
    print(f"is open: {cap.isOpened()}")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("break")
            break

        # Convert frame to base64
        img_str = frame_to_base64(frame)
        
        # Send frame via websocket
        print("send")
        ws.send(json.dumps({"data": img_str}))
        print("after send")

    print("close")

    cap.release()
    ws.close()

if __name__ == "__main__":
    async def test():
        async with websockets.connect('ws://raspberrypi:8000') as websocket:

            cap = cv2.VideoCapture('bad apple.mp4')

            fps = cap.get(cv2.CAP_PROP_FPS)
            ime_per_frame = 1 / fps
            fps_limit = 30
            time_per_frame = 1 / fps_limit

            start_time = time.time()

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    print("break")
                    break

                current_time = time.time()
                elapsed_time = current_time - start_time
                
                # Calculate the expected frame number
                expected_frame_number = int(elapsed_time * fps)
                print(expected_frame_number)
                
                # Set the video capture to the expected frame
                cap.set(cv2.CAP_PROP_POS_FRAMES, expected_frame_number)

                frame = cv2.resize(frame, (64, 64))

                # Convert frame to base64
                img_str = frame_to_base64(frame)

                await websocket.send(img_str)
                time.sleep(time_per_frame)
                #input("pause...")
                response = await websocket.recv()
                #print(response)

    asyncio.get_event_loop().run_until_complete(test())