#!/usr/bin/env python3
#coding: utf-8

from zencad import *

D = 52

base = cylinder(r=D/2, h=3)


m = (
	base 
	- box(24, 12, 3, center = True).up(1.5).left(6)
	+ box(6, 12, 3, center = True).up(4.5).left(21)
	+ box(6, 12, 3, center = True).up(4.5).right(9)
	- cylinder(r =0.75, h = 6).right(8)

	- cylinder(r =0.75, h = 6).right(8-28)
)

display(m)
show()