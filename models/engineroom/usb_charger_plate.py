#!/usr/bin/env python3
#coding: utf-8

from zencad import *
from params import *

x=19
y=25
t=1

bx=7.5
by=9.5
bz=3.8

bd = 0.5

s=2
shift = -13

on_z=7
on_x=13
on_y=9.5


xw = 5
yw = 2
zw = 1

usb_charger_position = rotateZ(gr(180)) * translate(shift, body_y/2 - y/2 - bottom_wall_thikness, bottom_wall_thikness)
on_position = rotateZ(gr(180)) * translate(-shift, body_y/2 - bottom_wall_thikness, bottom_wall_thikness + 1 + on_z/2)

def usb_charger_top():
	return box(bx,by,bz, center=True).up(bz/2+t/2).forw(y/2-by/2+s)

def usb_charger_top_hole():
	return box(bx+bd*2,by+bd*2,bz+bd*2, center=True).up(bz/2+t/2).forw(y/2-by/2+s).up(t/2)

def usb_charger():
	return (box(x,y,t, center=True) + usb_charger_top())

def on_hole():
	return box(on_x, on_y, on_z, center=True)

def usb_charger_protect():
	m = ( box(x + xw*2, by+yw, bz+t + zw)
	 -box(bx, by, bz).right((x + xw*2-bx)/2).up(t)
	 -box(x, by+yw, t).right(xw)
	 -multitransform([translate(xw/2,(yw+by)/2,0), translate(x+xw*3/2,(yw+by)/2,0)])(cylinder(r=1.5, h=bz+zw+t))
	).translate(-(x + xw*2)/2, -(by+yw)/2 - y/2 + (by+s)/2, -t/2).rotateZ(gr(180))
	return m

def usb_charger_protect_hole():
	return multitransform([translate(xw/2,(yw+by)/2,0), translate(x+xw*3/2,(yw+by)/2,0)])(cylinder(r=1.5, h=bz+zw+t)).translate(-(x + xw*2)/2, -(by+yw)/2 - y/2 + (by+s)/2, -t/2).rotateZ(gr(180))


if __name__ == "__main__":
	display(usb_charger() + usb_charger_protect())
	#display(usb_charger_protect_hole())
	show()