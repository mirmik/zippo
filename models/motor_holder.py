#!/usr/bin/env python3
#coding: utf-8

from zencad import *
zencad.lazy.fastdo=True

xgate = 14.65
ygate = 11.6
zgate = 11
t = (xgate - 11.7) / 2

ear_r = 8.6/2
ear_w = 7.8 - ear_r
ear_z = 3

hx_h = 2.0

bx = xgate + ear_w
by = 2
bz = ear_z+1

gate = (
	box(xgate, ygate, t).up(zgate - t) +
	box(t, ygate, zgate) +
	box(t, ygate, zgate).right(xgate - t)
)
gate = gate.fillet(1, [5, 23, 29, 76])
gate = gate.left(xgate/2)

ear = (box(ear_w, ear_r * 2, ear_z) + cylinder(r = ear_r, h = ear_z).forw(ear_r).right(ear_w)).right(xgate/2 - t)
hx = linear_extrude( ngon(r = 2.5, n = 6).rotateZ(deg(90)).forw(ear_r), hx_h ).up(ear_z - hx_h).right(xgate/2 -t  + ear_w)

m = (
	gate 
	
	+ ear 
	+ ear.mirrorYZ() 
	
	- hx 
	- hx.mirrorYZ() 
	
	- box(xgate-2*t, ygate, zgate, center = True).forw(ygate/2)

	- box(bx, by, bz, center = True).forw(ear_r).up(bz/2)

	- cylinder(r = 2/2, h = 100, center = True).right(xgate/2-t+ear_w).forw(ear_r)
	- cylinder(r = 2/2, h = 100, center = True).left(xgate/2-t+ear_w).forw(ear_r)
)
display(m)
#display(gate)
show()