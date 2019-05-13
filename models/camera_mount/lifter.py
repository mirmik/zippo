#!/usr/bin/env python3

from zencad import *

w = 54
l = 34
r = 8
t = 3
h = 30

m = box(w, t, h)
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

hole = rotate_array(n=4)(cylinder(r=0.5, h=t).forw(7))

hl(hole)

m = (
	m 
	+ ear	
	+ cyltrans(cyl)
	- cyltrans(hole)
)

disp(m)
show()