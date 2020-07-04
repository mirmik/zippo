#!/usr/bin/env python3

from zencad import *

lazy.fastdo=True

class RotaryBase:
	t=2 
	roof_r=40
	spike_n=8
	spike_r1=3
	spike_r2 = roof_r - spike_r1 - t
	light_r = 6
	motor_hole = cylinder(r=5.5, h=t) - halfspace().rotateX(deg(90)).moveY(5)
	light_holes = rotate_array(spike_n)(cylinder(r=light_r, h=t).left(roof_r-light_r-t).rotateZ(deg(360/8/2)))

	nut_hole1 = rotate_array(4)((cylinder(r=1,h=t)+cone(r1=1,r2=2,h=t/2).up(t/2)).left(roof_r-t-2).rotateZ(deg(360/40)))
	nut_hole2 = rotate_array(4)((cylinder(r=1,h=t)).left(roof_r-t-2).rotateZ(deg(360/40)))
		
	border_t=3 

	@staticmethod
	def cables_hole():
		t = RotaryBase.t
		pnts = points([(17,0), (0,-10), (-17,0)])
		spine = interpolate(pnts)
		chole_width = 5
		tt = spine.d1(0)
		pt = tt.cross(vector(0,0,1)).normalize()
		perp = segment(point(pt*chole_width/2), point(-pt*chole_width/2))
		cables_hole = pipe(profile=perp.move(*pnts[0]), spine=spine) \
			+ circle(chole_width/2).move(*pnts[0]) + circle(chole_width/2).move(*pnts[-1])
		return cables_hole.extrude(t) 
		
	def roof(self):
		r = self.roof_r + self.border_t
		r1 = r + 5
		t = self.t
		c_h = 10

		base = (cylinder(r=r, h=t) 
			- self.light_holes 
			- self.motor_hole
			- self.nut_hole2
			- self.cables_hole()
		)

		#c = (cone(r1=r, r2=r1, h=c_h) - cone(r1=r-t, r2=r1-t, h=c_h)).up(t)

		mh = (
			box(31,1,2,center=True) 
			+ box(1,15,2,center=True).moveY(7.5) 
			+ cylinder(r=2.5,h=2,center=True).moveX(31/2)
			+ cylinder(r=2.5,h=2,center=True).moveX(-31/2)
			- cylinder(r=1,h=2,center=True).moveX(31/2)
			- cylinder(r=1,h=2,center=True).moveX(-31/2)
		).up(t+1).moveY(5+0.5)

		return unify(base + mh)

	def stolb(self,r1,r2,r3,h1,angles=(deg(0),deg(90),deg(180),deg(270))):
		b = cylinder(r=r1,h=h1)
		tri = polygon([(0,0),(0,h1),(r3,0)])
		tri = tri.extrude(self.t, center=True)

		for d in angles:
			b = b + tri.rotateX(deg(90)).rotateZ(d)

		return (b 
			- cylinder(r=r2,h=h1)
		)

	def room(self):
		y=100
		t=self.t
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
			self.stolb(srad,ir,7,k,angles=[deg(0),deg(180),deg(270)]).move(x_ext/2+srad,y-3-t*1-1,0),
			self.stolb(srad,ir,7,k,angles=[deg(0),deg(180),deg(270)]).move(x-x_ext/2-srad,y-3-t*1-1,0),
			self.stolb(srad,ir,7,k).move(x_ext/2+srad,y-3-t*1-1-35,0),
			self.stolb(srad,ir,7,k).move(x-x_ext/2-srad,y-3-t*1-1-35,0)
		])

		return unify(
			base - panel.bbox().shape() + panel
			- roof_trans(cylinder(r=self.roof_r, h=t))
			+ roof_trans(self.roof())
			+ spi_kreps
		)

	def fork(self):
		h = 15
		hear_x = 95/2
		hear_z = 50
		hear_R = 28/2
		hear_h = 15

		yk = hear_R * 3 / 4
		R = self.roof_r - self.t/2
		iR = self.roof_r - self.t/2 - self.t

		xk = math.sqrt(R**2 - yk**2)
		ixk = math.sqrt(iR**2 - yk**2)
		print(xk)

		base_cylinder = cylinder(r=R, h=h)
		ibase_cylinder = cylinder(r=iR, h=h - self.t) 
		base = (base_cylinder
			- halfspace().rotateY(deg(90)).moveX(-xk)
			- halfspace().rotateY(deg(-90)).moveX(xk)
		)

		ibase_cylinder = (ibase_cylinder
			- halfspace().rotateY(deg(90)).moveX(-ixk)
			- halfspace().rotateY(deg(-90)).moveX(ixk)
		)

		#face0 = near_face(base, point3(-1000,0,h/2))
			# - ibase_cylinder 

		hear_c = cylinder(r=hear_R, h=hear_h).rotateY(deg(-90))
		hear = hear_c
		hear = hear.move(-hear_x, 0 , hear_z)
		
		bx=hear_h;by=hear_R*6/4;bz=(hear_z-h)/2
		bbb = box(bx,by,bz,center=True).move(-hear_x - bx/2, 0 , hear_z-bz/2)
		ibbb = box(bx-self.t,by-2*self.t,bz,center=True).move(-hear_x - bx/2 +self.t/2, 0 , hear_z-bz/2)

		botwire1 = near_face(bbb, point(-hear_x-bx/2, 0, -10000)).wires()[0]
		#botwire2 = botwire1.move(-botwire1.props1().center())
		#botwire2 = botwire2.moveX(-self.roof_r/2)
		#
		ibotwire1 = near_face(ibbb, point(-hear_x-bx/2, 0, -10000)).wires()[0]
		#ibotwire2 = ibotwire1.move(-ibotwire1.props1().center())
		#ibotwire2 = ibotwire2.moveX(-self.roof_r/2 + self.t)
#
		botwire2 = botwire1.move(hear_x - xk + hear_h, 0, -hear_z+bz)
		ibotwire2 = ibotwire1.move(hear_x - ixk + hear_h, 0, -hear_z+bz)

		hear += bbb
		hear += loft([botwire1, botwire2])
		hear += hear.mirrorYZ()

		
		ihear_c = cylinder(r=23/2, h=hear_h - self.t).rotateY(deg(-90))
		ihear = ihear_c
		ihear = ihear.move(-hear_x, 0 , hear_z)
		ihear_c2 = (cylinder(r=6,h=bz,center=True)-halfspace().rotateY(deg(90)).left(bx/2-self.t)).move(-hear_x - bx/2, 0 , hear_z-bz/2)
		ihear_c2_face0 = near_face(ihear_c2, point(-hear_x-bx/2, 0, -10000))
		ihear_c2_face1 = near_face(ihear_c2, point(-hear_x-bx/2, 0, -10000)).move(hear_x - ixk + hear_h, 0, -hear_z+bz)
		ihear += ihear_c2 
		ihear  += loft([ihear_c2_face1.wires()[0], ihear_c2_face0.wires()[0]])
		ihear += ihear.mirrorYZ()
#
		middle = unify(
			base 
			+ hear
			- ihear
			- ibase_cylinder
		)

		#supports = (
		#	hear_c.move(-hear_x, 0 , hear_z)
		#	- ihear_c.move(-hear_x, 0 , hear_z)
			#+ near_face(bbb, point(-hear_x-bx/2, 0, -10000)).extrude(self.t)
			#- cylinder(r=6,h=20,center=True).move(-hear_x - bx/2, 0 , hear_z-bz/2)
		#)

		return unify(
			middle 
			#+ supports
			#+ supports.mirrorYZ()
		)

	def fork_half0(self):
		return self.fork() - halfspace().rotateY(deg(90))

	def fork_half1(self):
		return self.fork() - halfspace().rotateY(deg(-90))

	def rotation_plate(
			self,
			border_h=4
		):
		t = self.t
		r = self.roof_r
		spike_r1 = self.spike_r1
		spike_r2 = self.spike_r2
		border_t = self.border_t
		spike_n = self.spike_n
		light_r = self.light_r

		stub_size = (5,2,2)
		stub_r = 23
	
		
		base = cylinder(r=r, h=t)
		border = cylinder(r=r+border_t, h=border_h+t) - cylinder(r=r, h=border_h+t) 
		spikes = rotate_array(spike_n)(sphere(r=spike_r1).up(t).left(spike_r2)) - halfspace()
		stub = box(stub_size, center=True).up(t+stub_size[2]/2).left(stub_r)
	
		motor_hole = cylinder(r=6, h=t)
		light_hole = self.light_holes
	
		conic = cone(r1=r, r2=r+10, h=10).up(t+spike_r1)

		return unify(
			base
			+ border
			+ spikes
			+ stub
	
			- motor_hole
			- light_hole
			- self.cables_hole()
			- self.nut_hole1
			- conic
		)

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

			#+ (rectangle(w+wl+wr, h+hb+ht).move(-wl,-hb) - rectangle(w, h))
		)

		return unify(m).extrude(self.t)

#disp(RotaryBase().room())
#disp(RotaryBase().rotation_plate().down(RotaryBase().rotation_plate().bbox().zmax))
disp(RotaryBase().fork_half0())#.up(10))
#disp(RotaryBase().roof())

to_stl(RotaryBase().rotation_plate(), "/home/mirmik/models/spi_rotation_plate.stl", delta=0.1)
to_stl(RotaryBase().room(), "/home/mirmik/models/spi_room.stl", delta=0.1)
to_stl(RotaryBase().fork_half0(), "/home/mirmik/models/spi_forkhalf0.stl", delta=0.1)
to_stl(RotaryBase().fork_half1(), "/home/mirmik/models/spi_forkhalf1.stl", delta=0.1)

#disp(m)
show()

