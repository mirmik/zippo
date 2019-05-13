#!/usr/bin/env python3

import io

import numpy as np
import cv2
from PIL import Image

import pycrow as crow
import threading

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640); 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480);
cap.set(cv2.CAP_PROP_SATURATION,0.2);

crow.create_udpgate(12, 10010)
crow.set_crowker(".12.127.0.0.1:10009")

crow.diagnostic_enable()

thr = threading.Thread(target=crow.spin, args=())
thr.start()

while(True):
	ret, frame = cap.read()

	jpg = Image.fromarray(frame)
	tmpFile = io.BytesIO()
	jpg.save(tmpFile,'JPEG')

	tmpFile.seek(0)

	data = tmpFile.read()
	print(data[-40:-1])

	crow.publish("video_stream", data, 0, 200)

cap.release()
cv2.destroyAllWindows()