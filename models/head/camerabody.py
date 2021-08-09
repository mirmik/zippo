#!/usr/bin/env python3

from zencad import *
from globals import *

from stereopanel import plate
from topmotor_holder import TopMotorHolder

class CameraRoom(zencad.assemble.unit):


	def __init__(self):
		super().__init__()
		m = self.model()
		self.add(m)

	def model(self):
		PLATE_ANGLE = -50
		#m = box(100,20,30,center=True)
		p = plate(T)

		HEAR_RADIUS = 10

		X = p.bbox().xmax - p.bbox().xmin + 2*T 
		Z = p.bbox().ymax - p.bbox().ymin + 2*T
		ZU = 15
		Y = 100

		m = box(X,Y,Z+ZU, center=True)
		m -= box(X-2*T,Y-T,Z-T+ZU, center=True).move(0,T/2,T/2)

		m = m.up(ZU/2)

		p2 = p.rotX(deg(90)).rotY(deg(180)).movY(-Y/2+T/2)
		#disp(p2, color(0,1,0,0.9))
		m -= p2.bbox().shape()
		m += p2

		m -= cylinder(r=HEAR_RADIUS,h=1000, center=True).rotY(deg(90)).up(2)

		FAKEL_Z = 7
		s = sphere(r=5) + cylinder(r=5,h=FAKEL_Z)
		BSIZE = (10,10,10)
		BBOX = box(X,Y,Z+ZU, center=True).up(ZU/2).bbox().shape()
		m += box(BSIZE, center=True).move(X/2-BSIZE[0]/2, Y/2-BSIZE[1]/2-T, -Z/2+BSIZE[2]/2)
		m += box(BSIZE, center=True).move(-X/2+BSIZE[0]/2, Y/2-BSIZE[1]/2-T, -Z/2+BSIZE[2]/2) 
		m += s.move(-X/2+BSIZE[0]/2-5/2, Y/2-BSIZE[1]/2-T, Z/2+ZU-T-FAKEL_Z) ^ BBOX
		m += s.move(X/2-BSIZE[0]/2+5/2, Y/2-BSIZE[1]/2-T, Z/2+ZU-T-FAKEL_Z) ^ BBOX
		m += s.move(-X/2+BSIZE[0]/2-5/2, -Y/2+BSIZE[1]/2+T, Z/2+ZU-T-FAKEL_Z) ^ BBOX
		m += s.move(X/2-BSIZE[0]/2+5/2, -Y/2+BSIZE[1]/2+T, Z/2+ZU-T-FAKEL_Z) ^ BBOX

		m -= cylinder(r=1.8,h=8).move(-X/2+BSIZE[0]/2-5/2 + 2, Y/2-BSIZE[1]/2-T, Z/2+ZU-T-FAKEL_Z)
		m -= cylinder(r=1.8,h=8).move(X/2-BSIZE[0]/2+5/2 - 2, Y/2-BSIZE[1]/2-T, Z/2+ZU-T-FAKEL_Z)
		m -= cylinder(r=1.8,h=8).move(-X/2+BSIZE[0]/2-5/2 + 2, -Y/2+BSIZE[1]/2+T, Z/2+ZU-T-FAKEL_Z)
		m -= cylinder(r=1.8,h=8).move(X/2-BSIZE[0]/2+5/2 - 2, -Y/2+BSIZE[1]/2+T, Z/2+ZU-T-FAKEL_Z)

		p1 = point((90-5)/2, (40-5)/2,-Z/2).rotZ(deg(PLATE_ANGLE))
		p2 = point((90-5)/2, -(40-5)/2,-Z/2).rotZ(deg(PLATE_ANGLE))
		p3 = point(-(90-5)/2, -(40-5)/2,-Z/2).rotZ(deg(PLATE_ANGLE))
		p4 = point(-(90-5)/2, (40-5)/2,-Z/2).rotZ(deg(PLATE_ANGLE))
		
		CYLH = 10
		m += sqrmirror()(cylinder(r=2.5, h=CYLH).move((90-5)/2, (40-5)/2)).rotZ(deg(PLATE_ANGLE)).down(Z/2)
		m+= box(X/2-p1.x,5,CYLH,center=True).right((X/2-p1.x)/2).up(CYLH/2).move(p1)
		m+= box(5,Y/2+p2.y,CYLH,center=True).back((Y/2+p2.y)/2).up(CYLH/2).move(p2)
		m+= box(X/2+p3.x,5,CYLH,center=True).left((X/2+p3.x)/2).up(CYLH/2).move(p3)
		m+= box(X/2+p4.x,5,CYLH,center=True).left((X/2+p4.x)/2).up(CYLH/2).move(p4)

		m -= cylinder(r=1.8,h=10).rotX(deg(90)).move(X/2-5,Y/2-T,-Z/2+5)
		m -= cylinder(r=1.8,h=10).rotX(deg(90)).move(-X/2+5,Y/2-T,-Z/2+5)

		HHH = 4
		m+= ((rectangle(90,40, center=True).fillet(2.5) - rectangle(90-5-5/math.sqrt(2),40-5-5/math.sqrt(2), center=True)).extrude(HHH)
			.movZ(-Z/2+HHH/2).rotZ(deg(PLATE_ANGLE)))

		m -= sqrmirror()(cylinder(r=1.8/2, h=CYLH).move((90-5)/2, (40-5)/2)).rotZ(deg(PLATE_ANGLE)).down(Z/2)

		mh = (
			box(31,1,T,center=True) 
			+ box(1,15,T,center=True).moveY(7.5) 
			+ cylinder(r=2.5,h=T,center=True).moveX(31/2)
			+ cylinder(r=2.5,h=T,center=True).moveX(-31/2)
			- cylinder(r=1,h=T,center=True).moveX(31/2)
			- cylinder(r=1,h=T,center=True).moveX(-31/2)
		)

		#self.socket = zencad.assemble.unit(parent=self)
		#self.socket.down(Z/2-T).rotateZ(deg(-90)).forw(-9).left(40)

		XR = 10-T
		ZR = Z/2 - HEAR_RADIUS + T + HEAR_RADIUS*2
		YR = HEAR_RADIUS *2 + 4*T
		HEAR_RADIUS_IN = HEAR_RADIUS - 3
		c = box(XR,YR,HEAR_RADIUS+2*T, center=True).move(-X/2+XR/2 +T, 0, -HEAR_RADIUS/2-T)
		c += cylinder(r=HEAR_RADIUS+2*T, h=XR).rotY(deg(90)).move(-X/2+T,0,0)
		c -= (cylinder(r=HEAR_RADIUS,h=5) - cylinder(r=HEAR_RADIUS_IN, h=5)).rotY(deg(90)).movX(-X/2).up(T)
		c -= torus(r1=HEAR_RADIUS_IN, r2=3).rotY(deg(90)).movX(-X/2).left(-2).up(T)
		c -= motor_screw(3,5,3).rotZ(deg(90)).rotY(deg(90)).movX(-X/2).up(T).right(2)
		m = m+c

		return unify(m)

def plate_stereopi():
	X=90
	Y=40

	return box(X, Y, 1, center=True)

if __name__ == "__main__":
	croom = CameraRoom()
	#hld = TopMotorHolder()

	#croom.socket.link(hld)

	#hl(plate_stereopi().rotZ(deg(-50)))

	to_stl(croom.model(), "camerabody.stl",  0.01)
	disp(croom)
	show()
