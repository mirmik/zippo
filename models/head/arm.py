#!/usr/bin/env python3

from zencad import *
from globals import *

class Arm(zencad.assemble.unit):
	X = 16
	X2 = 30
	Y = 8
	H = 13.5
	H2 = 5

	Y2 = Y * math.sqrt(2)

	L0 = 12 
	L1 = L0 + 10

	def __init__(self):
		super().__init__()
		m = self.model()
		self.add(m)

	def model(self):
		#m = box(100, self.X, self.Y).back(self.X/2)
		#m -= box(100, self.X-2*T, self.Y-T).back(self.X/2).up(T).forw(T)
#
		#m=m.rotateY(deg(-45))
		##m -= box(self.W-2*T, self.W-T, self.W-T, center=True).move(0,T/2,T/2).up(self.W/2)
#
		#m -= halfspace().rotateY(deg(90))
		#m -= halfspace().mirrorXY().up(self.H)
#
		#m2 = (
		#	box(self.Y2, self.X, self.H2)
		#	- box(self.Y2 - T*math.sqrt(2), self.X-2*T, self.H2).move(0,T)
		#).move(self.H-self.Y2 ,-self.X/2,self.H)

		POINTS = points([
			(0,0),
			(-self.L1,self.H),
			(-self.L1,self.H+self.H2),
			(-self.L0,self.H+self.H2),
			(-self.L0,self.H),
			(0,15),
		])

		POINTS2 = points([
			(0,T),
			(-self.L1+T,self.H),
			(-self.L1+T,self.H+self.H2),
			(-self.L0,self.H+self.H2),
			(-self.L0,self.H),
			(0,15),
		])

		m = polygon(POINTS).rotX(deg(90)).rotZ(deg(180)).extrude((0,self.X,0), center=True)

		m -= polygon(POINTS2).rotX(deg(90)).rotZ(deg(180)).extrude((0,self.X-2*T,0), center=True)


#
		j = box(T, self.X + T * 4, 15).movY(-self.X/2-T*2)
		j -= box(T, self.X -2*T, 15).movY(-self.X/2+T).up(T)

		j -= halfspace().rotateY(deg(180)+math.atan2(POINTS[1].y-POINTS[0].y,POINTS[1].x-POINTS[0].x)) 
		#j -= halfspace().rotateY(deg(-45)) 

		m += j
		
		LLL = self.H+self.H2
#
		w2 = 12
		rrr = multitrans(
		[
			move(w2-0.5-T, 0, T+T),
			move(-w2+0.5+T, 0, T+T),
			move(w2-0.5-T, 0, 7+T+T),
			move(-w2+0.5+T, 0, 7+T+T),
		])(cylinder(r=1.9/2,h=1000, center=True).rotX(deg(90))).rotZ(deg(90))

		lll = box(self.Y2, self.X2, T, center=True)
		lll -= box(self.Y2  - T*math.sqrt(2), self.X - T*2, T, center=True).move(-T*math.sqrt(2)/2,0,0)

		lll = lll.move(self.L0+self.Y2/2,0,self.H+self.H2-T/2)

		m += lll

		#m -= sqrmirror()(cylinder(r=1.8/2,h=100).move(4, (self.X2-2*T)/2)).move(self.L0 + 5.5)

		m -= cylinder(r=1.8/2,h=100).move(self.L0 + 6, (self.X2 - T*2)/2)
		m -= cylinder(r=1.8/2,h=100).move(self.L0 + 6, -(self.X2 - T*2)/2)

		self.socket = zencad.assemble.unit(parent=self, location=
			move(self.L0,0,LLL))
		self.socket.add_triedron()

		return m - rrr


if __name__ == "__main__":
	module = Arm()
	to_stl(module.model(), "arm.stl", 0.01)
	disp(module)
	show()