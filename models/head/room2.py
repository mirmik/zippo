#!/usr/bin/env python3

from zencad import *
from globals import *

class Room(zencad.assemble.unit):
	motor_hole = cylinder(r=5.5, h=T) - halfspace().rotateX(deg(90)).moveY(5)

	def __init__(self):
		super().__init__()
		self.t = T
		self.bottom_place = 6 # место под платой stereopi
		self.roof_r = ROOF_R
		self.border_t = BORDER_T
		self.body = self.model()
		self.add(self.body)

	def model(self):
		y=100
		t=T
		x_ext = 6*t

		add_z_to_roof = 10
		add_z_to_down = 1

		plate_legs_size = self.bottom_place
		
		panel = self.panel()
		px = panel.bbox().xmax
		z = panel.bbox().ymax - panel.bbox().ymin + 2*t + add_z_to_roof + add_z_to_down
		x = panel.bbox().xmax + x_ext
		k = panel.bbox().ymax - panel.bbox().ymin - 5 - 1.6 + t + add_z_to_roof

		self.socket = zencad.assemble.unit(location=up(z-t), parent=self)

		self.x = x
		self.y = y

		base = box(x,y,z,center=True) - box(x-2*t,y-2*t,z-t,center=True).move(0,0,t/2)
		base = base.moveZ(z/2)

		panel = (
			panel
				.rotateX(deg(90))
				.move(
					- (panel.bbox().xmax + panel.bbox().xmin) / 2,
					- y/2 + t,#y - t,
					-panel.bbox().ymin + t))#z - t + panel.bbox().ymin - add_z_to_down))
		#roof_trans = move(x/2, y/2, -t)

		rf = 10
		_fakel = sphere(rf) + cylinder(r=rf, h=10) - cylinder(r=1.5, h=10).move(-2.5*t,-2.5*t)
		_fakel = _fakel.up(z)
		fakel = _fakel.move(x/2, y/2, -10-t)
		fakel = sqrmirror()(fakel)
		
		fakel2 = sphere(r=6).mov(x/2, 0, z-t)
		fakel2 += sphere(r=6).mov(-x/2, 0, z-t)
		fakel2 += sphere(r=6).mov(0, y/2, z-t)
		fakel2 += sphere(r=6).mov(0, -y/2, z-t)

		fakel += fakel2
		fakel -= box(x,y,t,center=True).up(z-t/2)


		# крепление для stereopi
		#print(k)
		srad=3
		ir = 1.8
		sh = plate_legs_size
		spi_kreps = union([
			stolb(srad,ir,7,sh).move(px/2-srad,-(y/2-3-t*1-0.5),0),
			stolb(srad,ir,7,sh).move(-px/2+srad,-(y/2-3-t*1-0.5),0),
			stolb(srad,ir,7,sh).move(px/2-srad,-(y/2-3-t*1-1-34.5),0),
			stolb(srad,ir,7,sh).move(-px/2+srad,-(y/2-3-t*1-1-34.5),0)
		]).up(t)

		spi_kreps2 = sqrmirror()(
			stolb(srad,ir,7,sh).move(35/2-3, 32/2-3),
		).up(t)

		ardu_kreps = sqrmirror()(
			stolb(2,1.8/2,7,sh).move(44/2-1, 18/2-1),
		).up(t)


		f = unify((
			base - panel.bbox().shape() + panel
			- multitrans([
				move(-x/2+t/2, -33, 5 + 2) * rotateZ(deg(90)) * rotateX(deg(90)),
			])(widewire(segment((0,0),(0,20)), r=4).extrude(T,center=True))
			#- box(2, y-2*t, t, center=True).movZ(t/2).movX(x/2-t-1)
			#- box(2, y-2*t, t, center=True).movZ(t/2).movX(-x/2+t+1)
			+ (fakel ^ base.bbox().shape())
			#- roof_trans(cylinder(r=ROOF_R, h=t))
			#+ roof_trans(self.roof())
			+ spi_kreps
			+ spi_kreps2.move(-25,+11)
			+ spi_kreps2.move(+25,+15)
			+ ardu_kreps.move(-21, 38)
		) ^ base.bbox().shape()) 

		#f = f.move(-x/2,-y/2,self.t).rotX(deg(180)).movZ(z)
		#self.socket = zencad.assemble.unit(parent=self, location=moveZ(z))

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
		g = self.bottom_place

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

if __name__ == "__main__":
	room = Room()
	disp(room)
	to_stl(room.body, "/home/mirmik/models/room2.stl", delta=0.1)
	show()