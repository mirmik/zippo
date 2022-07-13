#!/usr/bin/env python3

import tty
import os, sys
import pycrow
import time
import threading
import termios

import string
import signal
import random

pycrow.create_udpgate(12)
pycrow.start_spin()
pycrow.diagnostic_setup(True)

def sigint(code):
	pycrow.stop_spin()
	termios.tcsetattr(sys.stdin.fileno(), termios.TCSAFLUSH, oldterm)
	exit(0)
signal.signal(signal.SIGINT, sigint)		

requestor = pycrow.publisher(".12.192.168.1.100:10009", "zippo/ctr")

print("Connect")
requestor.publish("enable on".encode("utf-8"))

oldterm = termios.tcgetattr(sys.stdin.fileno())
tty.setraw(sys.stdin.fileno())
def getchar():
	import tty, termios, sys
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		ch = sys.stdin.read(1)
	finally:
		pass
		#termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch

speed = 0.22
rspeed = 0.21
while 1:
	print("Press Key")
	ch = getchar()
	print("You pressed", ch, ord(ch))

	requestor.publish("enable on".encode("utf-8"))
	if ch == 'q' or ord(ch) == 3: 
		break
	elif 'A' == ch:
		requestor.publish(("power %.2f %.2f"%(speed,speed)).encode("utf-8"))
		print("up")
	elif 'B' == ch:
		requestor.publish(("power -%.2f -%.2f"%(speed,speed)).encode("utf-8"))
		print("down")
	elif 'C' == ch:
		requestor.publish(("power %.2f -%.2f"%(rspeed,rspeed)).encode("utf-8"))
		print("rigth")
	elif 'D' == ch:
		requestor.publish(("power -%.2f %.2f"%(rspeed,rspeed)).encode("utf-8"))
		print("left")
	elif 32 == ord(ch):
		requestor.publish("power 0 0".encode("utf-8"))
		print("stop")

	elif 'p' == ch:
		speed += 0.005
		print(speed)

	elif 'o' == ch:
		speed -= 0.005
		print(speed)


	elif 'l' == ch:
		rspeed += 0.005
		print(rspeed)

	elif 'k' == ch:
		rspeed -= 0.005
		print(rspeed)

cancel_token =True
pycrow.stop_spin(False)
termios.tcsetattr(sys.stdin.fileno(), termios.TCSAFLUSH, oldterm)