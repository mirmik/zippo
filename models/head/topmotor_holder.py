#!/usr/bin/env python3

from zencad import *
from globals import *

class TopMotorHolder(zencad.assemble.unit):
	H = 3

	Y = 11.5
	X = 20
	X2 = 30
	Z = 11

	def __init__(self):
		super().__init__()
		m = self.model()

		
		#self.relocate(move(-15,5,12+8) * rotateX(deg(90)))
		self.add(m)
		
		
	def model(self):
		m = cylinder(r=28/2+T, h=self.H) 
		m += widewire(segment((-21+3,0,0), (21-3,0,0)), 3.5+T).extrude(self.H)
		m += box(15+2*T, 17+T, self.H).movX(-15/2-T)

		m -= box(16, 17.5, self.H).movX(-16/2).up(T)
		m -= box(6,1000,1000).move(-3,0,T)
		m -= cylinder(r=29/2, h=self.H-T).up(T) 
		m -= (box(21*2-3*2, 8, self.H, center=True).up(T+self.H/2) 
				+ cylinder(r=4, h=self.H-T).movX(21-3).up(T)
				+ cylinder(r=4, h=self.H-T).movX(-21+3).up(T)
			)
		m -= cylinder(r=2,h=T).move(21-3,0,0)
		m -= cylinder(r=2,h=T).move(-21+3,0,0)
		m -= cylinder(r=5,h=T).movY(-8)

		m = m.rotX(deg(-90)).up(17+T).back(T)
		m = m.rotZ(deg(-90))#.rotX(deg(180))#.up(42.5)

		m = m.movX(T)

		r = box(self.Y , self.X2, 1.4).move(0, -self.X2/2)
		r -= box(9, 15, 1.4).move(0, -7.5)

		m += r

		m -= cylinder(r=1.8/2,h=100).move(6, (self.X2 - T*2)/2)
		m -= cylinder(r=1.8/2,h=100).move(6, -(self.X2 - T*2)/2)

		p = polygon([
			(0,0),
			(11,0),
			(0,8)
		]).extrude(T,center=True)

		p = p.rotX(deg(90))

		m += p.movY(self.X/2 - T/2)	
		m += p.movY(-self.X/2 +T/2)		

		m += cylinder(r=9.9,h=5).rotY(deg(-90)).up(27) - cylinder(r=8.5,h=5).rotY(deg(-90)).up(27) 

		j = (circle(10)-circle(r=8).move(1,0)).extrude(T).rotY(deg(90)).up(26.9)

		m+=j

		return m

	def holder(self):
		H = 8
		B = 8
		W = 8

		t = 1

		stif = polygon([
			(0,0),
			(H-T, 0),
			(0, B-T),
		]).extrude(t,center=True)

		stif = stif.rotateY(deg(-90)).up(T).forw(T)

		base = box(W,B,T).movX(-W/2)
		base2 = box(W,H,T).rotX(deg(90)).movY(T).movX(-W/2)
		
		m = (base + base2 
			+ stif.movX(W/2 - t/2)
			+ stif.movX(-W/2 + t/2)
		).movY(-B)

		m -= cylinder(r=2, h=1000, center=True).rotX(deg(90)).up(H/2 + T/2)

		return m

if __name__ == "__main__":
	module = TopMotorHolder()
	disp(module)
	to_stl(module.model(), "topmotor_holder.stl", delta=0.1)
	show()