#!/usr/bin/env python3
#coding: utf-8

from zencad import *

s = box(5,3,15) - cylinder(h=3, r=1).rotateX(gr(90)).up(15/2+3/2).forw(3).right(5/2)

m = (
	box(34, 10, 1.5) 
	+ s.right(29)
	+ s
	- cylinder(h=3, r=1).forw(6.5).right(5/2)
	- cylinder(h=3, r=1).forw(6.5).right(5/2 + 29)
)


display(m)
show()