#!/usr/bin/env python3

from flask import Flask, Response
import threading
import cv2

lock = threading.Lock()
app = Flask(__name__)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

iii = 0

def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock, iii
    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # generate random output frame    
            ret, frame = cap.read()

            iii += 1
            if iii % 5 == 0:
                iii = 0

            quality = 30
            if iii % 0 == 0:
                quality = 50

            # encode the frame in JPEG format
            print("Generating frame...")
            (flag, encodedImage) = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
            # ensure the frame was successfully encoded
            if not flag:
                continue
        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')

@app.route("/")
def hello() -> str:
    return "Hello World"

@app.route("/video_feed")
def video_feed():
    return Response(generate(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(debug=False, port=15001, host="0.0.0.0")
