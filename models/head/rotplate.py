#!/usr/bin/env python3

from zencad import *
from globals import *

from room2 import Room

class RotationPlate(zencad.assemble.unit):
	def __init__(self):
		super().__init__()

		self.x = Room().x - 2*T
		self.y = Room().y - 2*T
		
		self.add(self.model())
		
		
	def model(
			self,
			border_h=4
		):
		t = T
		r = ROOF_R
		spike_r1 = SPIKE_R1
		spike_r2 = SPIKE_R2
		border_t = BORDER_T
		spike_n = SPIKE_N
		light_r = LIGHT_R

		stub_size = (5,2,2.7)
		stub_r = 28
	
		basebox = box(self.x, self.y, t, center=True).up(t/2)		
		base = cylinder(r=r, h=t)
		border = cylinder(r=r+border_t, h=border_h+t) - cylinder(r=r, h=border_h+t) 
		spikes = rotate_array(spike_n)(sphere(r=spike_r1).up(t).left(spike_r2)) - halfspace()
		stub = box(stub_size, center=True).up(t+stub_size[2]/2).left(stub_r)
	
		motor_hole = cylinder(r=5.2, h=t)
		light_hole = LIGHT_HOLES
	
		conic = cone(r1=r, r2=r+10, h=10).up(t+spike_r1)

		motor_socket = (
			cylinder(r=2,h=t).mov(35/2, -8)
			+ cylinder(r=2,h=t).mov(-35/2, -8)
		)

		self.socket = zencad.assemble.unit(parent=self, location=moveZ(spike_r1+T))

		
		m = unify(
			base
			+ basebox
			+ border
			+ spikes
			+ stub
	
			- motor_hole
			- light_hole
			- cables_hole().extrude(T).rotZ(deg(180))
			
		#	- NUT_HOLE1
			- conic
			- motor_socket

			- sqrmirror()(cylinder(r=1.5,h=t).mov(self.x/2-t*1.5,self.y/2-t*1.5))
		)

		m = fillet(m, r=0.7, refs=[point3(10,0,0), (10,0,t)])

		m -= box(T,20,T,center=True).movZ(T/2).mov(self.x/2-T/2)

		return m

if __name__ == "__main__":
	rotplate = RotationPlate()
	disp(rotplate)
	to_stl(rotplate.model(), "/home/mirmik/models/rootplate.stl", delta=0.1)
	show()