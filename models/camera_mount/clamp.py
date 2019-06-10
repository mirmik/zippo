#!/usr/bin/env python3

from zencad import *

w = 54
l = 34
r = 8
t = 3
h = 30

ww = 15

m = box(w + ww*2, t, h).left(ww)
ear = (polygon([
	(0,0), 
	(22, 0), 
	 zencad.util.circle_tangent_points(center=point3(22, 8), radius=8, point=point3(0, h))[1],
	(0, h)])
	.extrude(3)
		.rotateX(deg(90))
			.rotateZ(deg(90))
				.forw(3)
)

cyltrans = forw(22 + t) * up(r) * rotateY(deg(90))

cyl = cylinder(r=r, h=t)
chole = cylinder(r=2, h=t)
chole2 = cylinder(r=1, h=t)
hole = rotate_array(n=4)(cylinder(r=0.5, h=t).forw(6.5))

#m = (
#	m 
#	+ (ear	
#		+ cyltrans(cyl)
#		- cyltrans(chole2))
#	+ (ear
#		+ cyltrans(cyl) 
#		- cyltrans(hole)
#		- cyltrans(chole)
#	).right(w-t)
#)
#
m = (
	m 
	- multitrans([
		nulltrans(), 
		up(h/2),
		up(h/2) * right(ww + w),
		right(ww + w)
	])(cylinder(r=1.7, h=3).rotateX(deg(-90)).left(ww/2).up(h/4))
)
#
m = m.rotateX(deg(90))
#
##m = fillet(m, 3, refs = [
##	point3(50.901,-15.006,3.000), 
##	point3(3.000,-13.778,3.118),
##	point3(0.000,-13.543,3.842),
##	point3(54.000,-13.981,3.032)
##])
#
#m = unify(m)

disp(m)
show()