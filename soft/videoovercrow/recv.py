#!/usr/bin/env python3

import io

import numpy as np
import cv2
import fcntl, os
from PIL import Image

import pycrow as crow
import threading

crow.create_udpgate(12, 10011)
crow.set_crowker(".12.192.168.1.93:10009")

thr = threading.Thread(target=crow.spin, args=())
thr.start()

#crow.diagnostic_enable()

data = None
def handler(pack):
	global data
	data = pack.data()
	#print(data[-40:-1])

crow.subscribe("video_stream", handler, qos=0, ackquant=200, rqos=0, rackquant=200)

while(True):
	if (data is not None):
		#print(len(data))
		tmpFile = io.BytesIO()
		tmpFile.write(data)
		tmpFile.seek(0)
	
		img = Image.open(tmpFile)
		I = np.asarray(img)
		I=cv2.flip(I, -1);
		#I = cv2.resize(I,(int(640), int(480)))
		I = cv2.resize(I,(int(640*3/2), int(480*3/2)))
		
		cv2.imshow('frame',I)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

cap.release()
cv2.destroyAllWindows()