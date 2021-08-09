#!/usr/bin/env python3

from zencad import *

T=2
ROOF_R=40
SPIKE_N = 8
LIGHT_R = 6
LIGHT_HOLES = rotate_array(SPIKE_N)(cylinder(r=LIGHT_R, h=T).left(ROOF_R-LIGHT_R-T).rotateZ(deg(360/8/2)))
BORDER_T = 3

SPIKE_R1=3
SPIKE_R2 = ROOF_R - SPIKE_R1 - T

NUT_HOLE1 = rotate_array(4)((cylinder(r=1,h=T)+cone(r1=1,r2=2,h=T/2).up(T/2)).left(ROOF_R-T-2).rotateZ(deg(360/40)))
NUT_HOLE2 = rotate_array(4)((cylinder(r=1,h=T)).left(ROOF_R-T-2).rotateZ(deg(360/40)))

def motor_screw(r, h, f):
	c = cylinder(r, h)
	c -= halfspace().rotateX(deg(90)).moveY(f/2)
	c -= halfspace().rotateX(-deg(90)).moveY(-f/2)
	return c 

def cables_hole():
	t = T
	pnts = points([(17,0), (0,-10), (-17,0)])
	spine = interpolate(pnts)
	chole_width = 5
	tt = spine.d1(0)
	pt = tt.cross(vector(0,0,1)).normalize()
	perp = segment(point(pt*chole_width/2), point(-pt*chole_width/2))
	cables_hole = pipe(profile=perp.move(*pnts[0]), spine=spine) \
		+ circle(chole_width/2).move(*pnts[0]) + circle(chole_width/2).move(*pnts[-1])
	return cables_hole.extrude(t) 

def stolb(r1,r2,r3,h1,angles=(deg(0),deg(90),deg(180),deg(270))):
	b = cylinder(r=r1,h=h1)
	tri = polygon([(0,0),(0,h1),(r3,0)])
	tri = tri.extrude(T, center=True)

	for d in angles:
		b = b + tri.rotateX(deg(90)).rotateZ(d)

	return (b 
		- cylinder(r=r2,h=h1)
	)


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

class RotationPlate(zencad.assemble.unit):
	def __init__(self):
		super().__init__()
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

		stub_size = (5,2,2)
		stub_r = 23
	
		
		base = cylinder(r=r, h=t)
		border = cylinder(r=r+border_t, h=border_h+t) - cylinder(r=r, h=border_h+t) 
		spikes = rotate_array(spike_n)(sphere(r=spike_r1).up(t).left(spike_r2)) - halfspace()
		stub = box(stub_size, center=True).up(t+stub_size[2]/2).left(stub_r)
	
		motor_hole = cylinder(r=6, h=t)
		light_hole = LIGHT_HOLES
	
		conic = cone(r1=r, r2=r+10, h=10).up(t+spike_r1)

		self.socket = zencad.assemble.unit(parent=self, location=moveZ(spike_r1+T))

		return unify(
			base
			+ border
			+ spikes
			+ stub
	
			- motor_hole
			- light_hole
			- cables_hole().rotZ(deg(180))
			- NUT_HOLE1
			- conic
		)

class Fork(zencad.assemble.unit):
	def __init__(self):
		super().__init__()

	def fork(self):
		h = 15
		hear_x = 95/2
		hear_z = 44
		hear_R = 28/2
		hear_h = 15

		yk = hear_R * 3 / 4
		R = ROOF_R #- self.t/2
		iR = ROOF_R - T*2

		xk = math.sqrt(R**2 - yk**2)
		ixk = math.sqrt(iR**2 - yk**2)

		base_cylinder = cylinder(r=R, h=h)
		ibase_cylinder = cylinder(r=iR, h=h - T) 
		base = (base_cylinder
			- halfspace().rotateY(deg(90)).moveX(-xk)
			- halfspace().rotateY(deg(-90)).moveX(xk)
		)

		icyl = cylinder(r=R-T, h=T)

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
		ibbb = box(bx-T,by-2*T,bz,center=True).move(-hear_x - bx/2 +T/2, 0 , hear_z-bz/2)

		botwire1 = near_face(bbb, point(-hear_x-bx/2, 0, -10000)).wires()[0]
		botwire2 = botwire1.move(-botwire1.props1().center())
		botwire2 = botwire2.moveX(-ROOF_R/2)
		
		ibotwire1 = near_face(ibbb, point(-hear_x-bx/2, 0, -10000)).wires()[0]
		#ibotwire2 = ibotwire1.move(-ibotwire1.props1().center())
		#ibotwire2 = ibotwire2.moveX(-self.roof_r/2 + self.t)
#
		botwire2 = botwire1.move(hear_x - xk + hear_h, 0, -hear_z+bz)
		ibotwire2 = ibotwire1.move(hear_x - ixk + hear_h, 0, -hear_z+bz)
		
		hear += bbb
		hear += loft([botwire1, botwire2])
		hear += hear.mirrorYZ()

		
		ihear_c = cylinder(r=23/2, h=hear_h - T).rotateY(deg(-90))
		ihear0 = ihear_c
		ihear0 = ihear0.move(-hear_x, 0 , hear_z)
		ihear_c2 = (cylinder(r=6,h=bz,center=True)-halfspace().rotateY(deg(90)).left(bx/2-T)).move(-hear_x - bx/2, 0 , hear_z-bz/2)
		ihear_c2_face0 = near_face(ihear_c2, point(-hear_x-bx/2, 0, -10000))
		ihear_c2_face1 = near_face(ihear_c2, point(-hear_x-bx/2, 0, -10000)).move(hear_x - ixk + hear_h, 0, -hear_z+bz-T*2.5)
		ihear0 += ihear_c2 
		ihear0 += loft([ihear_c2_face1.wires()[0], ihear_c2_face0.wires()[0]])
		ihear0 += sphere(12).move(-iR+10,0,0)
#
		ihear1 = cylinder(r=20/2, h=hear_h - T)
		ihear1 += box(12*2,T,hear_h-T,center=True).movZ((hear_h-T)/2)
		ihear1 += box(T,12*2,hear_h-T,center=True).movZ((hear_h-T)/2)
		ihear1 = ihear1.rotateY(deg(90)).move(hear_x, 0 , hear_z)


		middle = unify(
			base 
			+ hear
			- ihear0
			- ihear1
			- ibase_cylinder
			- icyl
		)

		stlb = (stolb(2.5,1.5,7,h-T*2,[deg(90),deg(180),deg(270)])
			.mirrorXY())#.rotZ(deg(45)))
		supports = sqrmirror()(
			stlb.move(ROOF_R-10, 0, h-T).rotZ(deg(45))
		)

		return unify(
			middle 
			+ supports
			#+ supports.mirrorYZ()
		)

class Fork0(Fork):
	def __init__(self):
		super().__init__()
		self.add(self.model())

	def model(self):
		return self.fork() - halfspace().rotateY(deg(90))

class Fork1(Fork):
	def __init__(self):
		super().__init__()
		self.add(self.model())

	def model(self):
		return self.fork() - halfspace().rotateY(deg(-90))

class ConnectionCylinder(zencad.assemble.unit):
	def __init__(self):
		super().__init__()
		self.add(self.model())

	def model(self):
		m = cylinder(ROOF_R-T, T)
		m -= motor_screw(3,5,3)

		m += sqrmirror()(
			(cylinder(r=4,h=3) - cylinder(r=3,h=3))
				.move(ROOF_R-10, 0, T).rotZ(deg(45)) 
			)
		m -= cables_hole().mirrorXZ()
		return m

class RotaryBase:
		
	def roof(self):
		r = self.roof_r + self.border_t
		r1 = r + 5
		t = self.t
		c_h = 10

		base = (cylinder(r=r, h=t) 
			- LIGHT_HOLES 
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
			stolb(srad,ir,7,k,angles=[deg(0),deg(180),deg(270)]).move(x_ext/2+srad,y-3-t*1-1,0),
			stolb(srad,ir,7,k,angles=[deg(0),deg(180),deg(270)]).move(x-x_ext/2-srad,y-3-t*1-1,0),
			stolb(srad,ir,7,k).move(x_ext/2+srad,y-3-t*1-1-35,0),
			stolb(srad,ir,7,k).move(x-x_ext/2-srad,y-3-t*1-1-35,0)
		])

		return unify(
			base - panel.bbox().shape() + panel
			- roof_trans(cylinder(r=self.roof_r, h=t))
			+ roof_trans(self.roof())
			+ spi_kreps
		)
	
	def crest(self):
		r = 20
		h = 10
		m = box(r, self.t, h, center=True) + box(self.t, r, h, center=True) 
		m = m.moveZ(h/2)
		return m

	
	def camera_box(self):
		x=80
		#ch = 4

		m = box(x, 30, 30, center=True)
		m -= (box(x-self.t*2, 30-self.t, 30-self.t, center=True)
			.move(0,-self.t,self.t))


		#m += cylinder(r=10,h=10).rotateY(deg(-90)).movX(-x/2)
		m -= cylinder(r=10,h=self.t).rotateY(deg(-90)).movX(-x/2+self.t)
		m -= cylinder(r=10,h=self.t).rotateY(deg(90)).movX(x/2-self.t)

		return m

room = Room()
rotplate = RotationPlate()
fork0 = Fork0()
fork1 = Fork1()
concyl = ConnectionCylinder()

room.socket.link(rotplate)
rotplate.socket.link(fork0)
rotplate.socket.link(fork1)
rotplate.socket.link(concyl)

disp(room)

#disp(Room())
#disp(RotaryBase().room().rotateX(deg(180)).move(-50, 50, -10))
#disp(RotaryBase().rotation_plate().rotZ(deg(180)).down(RotaryBase().rotation_plate().bbox().zmax))
#disp(RotaryBase().fork_half0())
#disp(RotaryBase().fork_half1())
#disp(RotaryBase().camera_box().moveZ(45))
#disp(RotaryBase().connection_cylinder())#.up(10))

#disp(RotaryBase().roof())

#to_stl(RotaryBase().rotation_plate(), "/home/mirmik/models/spi_rotation_plate.stl", delta=0.1)
#to_stl(RotaryBase().room(), "/home/mirmik/models/spi_room.stl", delta=0.1)
#to_stl(RotaryBase().fork_half0(), "/home/mirmik/models/spi_forkhalf0.stl", delta=0.1)
#to_stl(RotaryBase().fork_half1(), "/home/mirmik/models/spi_forkhalf1.stl", delta=0.1)

#disp(m)
show()

