#!/usr/bin/env python3
#coding: utf-8

from zencad import *
from drive_place import drive_place

x = 100
y = 150
z = 15
t = 1.5

s = y/4
sl = 40

#a = mirrorXZ()
#b = translate(+x/4,-y/2,0)

stiffener = linear_extrude(polygon(points([ 
	(0,0), (z,0), (0,z*2)
])),(0,0,t),center=True).rotateY(gr(-90))

stiffer_trans = multitransform([
	translate(-x/4,-y/2,0),
	translate(+x/4,-y/2,0),
	mirrorXZ() * translate(-x/4,-y/2,0),
	mirrorXZ() * translate(+x/4,-y/2,0),
	translate(+x/2,-s*3/8,0) * rotateZ(gr(90)),
	translate(-x/2,-s*3/8,0) * rotateZ(-gr(90)),
	translate(+x/2,s*3/8,0) * rotateZ(gr(90)),
	translate(-x/2,s*3/8,0) * rotateZ(-gr(90)),
])

sqtrans = multitransform([
	translate(0,0,0),
	mirrorYZ(),
	mirrorXZ(),
	mirrorZ(),
])

m =  difference([
	linear_extrude(rectangle(x, y, center = True).fillet(5,[0,1,2,3]),(0,0,z)),
	linear_extrude(rectangle(x-2*t, y-2*t, center = True).fillet(5-t,[0,1,2,3]),(0,0,z-t)).up(t)
])

drive_place = drive_place(t,z,sl,t)

m = (m
	#Cylinders body
	+ sqtrans(cylinder(r=5,h=z).translate(x/2-5,y/2-5,0)) 
 	
 	#Cylinders holes
	- sqtrans(cylinder(r=3,h=z).translate(x/2-5,y/2-5,0))
 	
 	#Drive places
	- sqtrans(drive_place.translate(x/2-t, s, 0))

	+stiffer_trans(stiffener)
)


#display(stiffener)
display(m)
show()