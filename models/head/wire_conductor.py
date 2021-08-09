#!/usr/bin/env python3

from zencad import *
from globals import *

class WireConductor(zencad.assemble.unit):
	Y = 11.5

	X = 20
	X2 = 35

	Z = 11

	RADIUS = 9.8

	def __init__(self):
		super().__init__()
		m = self.model()
		self.add(m)

	def model(self):
		m = box(self.X,self.Y,self.Z).move(-self.X/2,0,0)
		m += box(self.X2,T,self.Z).move(-self.X2/2,0,0)
		m += cylinder(r=10,h=self.Z).movY(self.Y)

		m += cylinder(r=self.RADIUS,h=16).movY(self.Y)
		m -= cylinder(r=8,h=18).movY(self.Y).up(T)

		m -= box(self.X-2*T,self.Y,self.Z-2*T).move(-self.X/2+T,0,T)

		m = m.rotX(deg(90)).movY(self.Z).rotZ(-deg(90))

		m -= cylinder(r=1.8/2,h=100).move(6, (self.X2 - T*2)/2)
		m -= cylinder(r=1.8/2,h=100).move(6, -(self.X2 - T*2)/2)

		return m


if __name__ == "__main__":
	module = WireConductor()
	to_stl(module.model(), "wire_conductor.stl", 0.01)
	disp(module)
	show()