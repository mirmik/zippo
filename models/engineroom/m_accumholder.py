#!/usr/bin/python3
#coding: utf-8

import zencad
from zencad import *

t=2

x=40 
y=78
z=24

x2=2*x
y2=y-4*t
z2=12

hole_d = 3
hole_x = 19
hole_y = 55

def accumholder_model():
	return ( box(size=[x,y,z], center=True) 
		- box(size=[x-2*t,y-2*t,z-t],center=True).up(t) 
		- box(size=[x2,y2,z2],center=True).up((z-z2)/2)
		+ box(size=[t,y,z2],center=True).down((z-z2)/2)
		- sqrtrans()(cylinder(r=hole_d/2, h=1000, center = True).translate(hole_x/2, hole_y/2, 0))
	).up(z/2).rotateZ(deg(90))


if __name__ == "__main__":
	display(accumholder_model())
	show()