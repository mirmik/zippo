#!/usr/bin/env python3

from zencad import *
from globals import *

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

		middle -= cylinder(r=R, h=T).movZ(h-T)

		stlb = stolb2(2.5,1.5,h-T*2).mirrorXY()# + box(T,10,h-T/2-5, center=True).mov(0,0,h/2)
		supports = sqrmirror()(
			stlb.move(ROOF_R-10, 0, h-T).rotZ(deg(45))
		)

		return unify(
			middle 
		#	+ supports
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


if __name__ == "__main__":
	fork0 = Fork0()
	fork1 = Fork1()
	#disp(fork0.rotateY(deg(45)))
	disp(fork0)
	disp(fork1)


	
	to_stl(fork1.model(), "/home/mirmik/models/fork1.stl", delta=0.1)
	to_stl(fork0.model(), "/home/mirmik/models/fork0.stl", delta=0.1)
	
	show()