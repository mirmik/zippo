#!/usr/bin/env python3
#coding:utf-8

from zencad import *

t = 1.5
m = (
	box(size=(17.5 + 5*2, 28 + 5, t)) 
	+ box(17.5 + 5*2, t, 8+t)
	- box(8, t, 4).right((17.5+5*2)/2 - 4).up(t)
)

display(m)
show()