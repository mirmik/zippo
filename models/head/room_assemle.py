#!/usr/bin/env python3

from zencad import *

from room import Room
from rotplate import RotationPlate

class RoomAssemble (zencad.assemble.unit):
	def __init__(self):
		super().__init__()

		self.room = Room()
		self.rotplate = RotationPlate()

		self.link(self.room)
		self.room.socket.link(self.rotplate)


if __name__ == "__main__":
	disp(RoomAssemble())
	show()