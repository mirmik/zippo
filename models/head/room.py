#!/usr/bin/env python3

from zencad import *
from globals import *

class Room(zencad.assemble.unit):
	motor_hole = cylinder(r=5.5, h=T) - halfspace().rotateX(deg(90)).moveY(5)

	def __init__(self):
		super().__init__()
		self.t = T
		self.roof_r = ROOF_R
		self.border_t = BORDER_T
		self.add(self.model())

	def model(self):
		y=100
		t=T
		x_ext = 6*t

		add_z_to_roof = 10
		add_z_to_down = 1
		
		panel = self.panel()
		z = panel.bbox().ymax - panel.bbox().ymin + 2*t + add_z_to_roof + add_z_to_down
		x = panel.bbox().xmax + x_ext
		k = panel.bbox().ymax - panel.bbox().ymin - 5 - 1.6 + t + add_z_to_roof

		base = box(x,y,z) - box(x-2*t,y-2*t,z-t).move(t,t,t)
		base = base.moveZ(-t)

		panel = (panel.rotateX(deg(-90)).move(x_ext/2,y-t,z-t + panel.bbox().ymin- add_z_to_down))
		roof_trans = move(x/2, y/2, -t)

		# крепление для stereopi
		#print(k)
		srad=2.5
		ir = 1.8
		spi_kreps = union([
			stolb(srad,ir,7,k,angles=[deg(0),deg(180),deg(270)]).move(x_ext/2+srad,y-3-t*1-1,0),
			stolb(srad,ir,7,k,angles=[deg(0),deg(180),deg(270)]).move(x-x_ext/2-srad,y-3-t*1-1,0),
			stolb(srad,ir,7,k).move(x_ext/2+srad,y-3-t*1-1-35,0),
			stolb(srad,ir,7,k).move(x-x_ext/2-srad,y-3-t*1-1-35,0)
		])

		f = unify(
			base - panel.bbox().shape() + panel
			- roof_trans(cylinder(r=ROOF_R, h=t))
			+ roof_trans(self.roof())
			+ spi_kreps
		)

		f = f.move(-x/2,-y/2,self.t).rotX(deg(180)).movZ(z)
		self.socket = zencad.assemble.unit(parent=self, location=moveZ(z))

		return f

	def panel(self):
		w=90
		h=18 + 2
		fw=95
		fh=32

		wl=4
		wr=4
		hb=5
		ht=3
		g = 5

		tz = 1.6
		m= (
			rectangle(w, h+g).move(0,-g)
			- (
				  rectangle(14-5, 6-tz).moveX(5)
				+ rectangle(47-32, 15-tz).moveX(32)
				+ rectangle(65-50, 18-tz).moveX(50)
				+ rectangle(82-68, 8-tz).moveX(68)
			)
			.moveY(tz)
		)

		return unify(m).extrude(T)

	def roof(self):
		r = self.roof_r + self.border_t
		r1 = r + 5
		t = self.t
		c_h = 10

		base = (cylinder(r=r, h=t) 
			- LIGHT_HOLES 
			- self.motor_hole
			- NUT_HOLE2
			- cables_hole()
		)

		mh = (
			box(31,1,2,center=True) 
			+ box(1,15,2,center=True).moveY(7.5) 
			+ cylinder(r=2.5,h=2,center=True).moveX(31/2)
			+ cylinder(r=2.5,h=2,center=True).moveX(-31/2)
			- cylinder(r=1,h=2,center=True).moveX(31/2)
			- cylinder(r=1,h=2,center=True).moveX(-31/2)
		).up(t+1).moveY(5+0.5)

		return unify(base + mh)

if __name__ == "__main__":
	room = Room()
	disp(room)
	show()