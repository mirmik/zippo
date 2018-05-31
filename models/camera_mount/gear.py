#!/usr/bin/env python3
#coding: utf-8

from zencad import *

n = 20
ri = 3.8 / 2
ro = 5.2 / 2

angles1 = [gr(360)/n*i for i in range(0,n)]
angles2 = [gr(360)/n*i+gr(360)/n/2 for i in range(0,n)]

r0 = [point3(ri*math.cos(a), ri*math.sin(a)) for a in angles1]
r1 = [point3(ro*math.cos(a), ro*math.sin(a)) for a in angles2]

parr = [] 
for i in range(0,len(r0)):
	parr.append(r0[i])
	parr.append(r1[i])

pol = polygon(parr)

m = linear_extrude(circle(r=5) - pol, 2.5).up(1.5) + linear_extrude(circle(r=8) - circle(r=2.5/2), 1.5)

m = (m 
	- cylinder(r=0.5, h=1.5).right(6.5)
	- cylinder(r=0.5, h=1.5).left(6.5)
	- cylinder(r=0.5, h=1.5).forw(6.5)
	- cylinder(r=0.5, h=1.5).back(6.5)
)

display(m)

show()