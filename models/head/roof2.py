#!/usr/bin/env python3

from zencad import *
from globals import *

from room2 import Room

class Roof(zencad.assemble.unit):
	motor_hole = cylinder(r=5.5, h=T) - halfspace().rotateX(deg(90)).moveY(5)

	def __init__(self):
		super().__init__()

		self.x = Room().x - 2*T -T/2
		self.y = Room().y - 2*T -T/2
		
		self.t = T
		self.roof_r = ROOF_R
		self.border_t = BORDER_T
		self.body = self.roof()
		self.add(self.body)

	def  roof(self):
		r = self.roof_r + self.border_t
		r1 = r + 5
		t = self.t
		c_h = 10

		base = (box(self.x, self.y, t, center=True).up(t/2) 
			- LIGHT_HOLES 
			- self.motor_hole
			- NUT_HOLE2
			- cables_hole().extrude(T)
		)

		mh = (
			box(31,1,T,center=True) 
			+ box(1,15,T,center=True).moveY(7.5) 
			+ cylinder(r=2.5,h=T,center=True).moveX(31/2)
			+ cylinder(r=2.5,h=T,center=True).moveX(-31/2)
			- cylinder(r=1,h=T,center=True).moveX(31/2)
			- cylinder(r=1,h=T,center=True).moveX(-31/2)
		).up(t+1).moveY(5+0.5)

		return unify(
			base 
			+ mh
			- sqrmirror()(cylinder(r=2.5/2,h=t).move(self.x/2 - T, self.y/2 - T)))

if __name__ == "__main__":
	room = Roof()
	disp(room)
	to_stl(room.body, "/home/mirmik/models/roof2.stl", delta=0.1)
	show()