#!/usr/bin/env python3
#coding: utf-8

from zencad import *
from params import *

#Размеры платы
x=19
y=25
t=1 #толщина платы

#Габариты usb порта.
bx=7.5 
by=9.5
bz=3.8

#зазор между портом и стенкой.
bd = 0.5

s=2
shift = -13

#Параметры выключателя.
on_z=8.3
on_x=13.1
on_y=9.5

upper_z = 3 #Высота подставки
upper_s = 4.5 #Отступы от краёв(под пайку)

xw = 5
yw = 2
zw = 1


usb_charger_position = rotateZ(gr(180)) * translate(shift, body_y/2 - y/2 - bottom_wall_thikness, bottom_wall_thikness)
on_position = rotateZ(gr(180)) * translate(-shift, body_y/2 - bottom_wall_thikness, bottom_wall_thikness + 2.5 + on_z/2)

#подставка под плату. (переносит пот немного выше)
def usb_plate_upper():
	return (box(t, y-upper_s, upper_z, center = True).left(x/2-t/2) + box(t, y-upper_s, upper_z, center = True).right(x/2-t/2)).up(upper_z/2).forw(upper_s/2)

def usb_charger_port():
	return box(bx,by,bz, center=True).up(bz/2+t/2).forw(y/2-by/2+s)

def usb_charger_port_hole():
	return box(bx+bd*2,by+bd*2,bz+bd*2, center=True).up(bz/2+t/2).forw(y/2-by/2+s).up(t/2).up(upper_z)

def usb_charger():
	return (box(x,y,t, center=True) + usb_charger_port()).up(t/2).up(upper_z)

def on_hole():
	return box(on_x, on_y, on_z, center=True)

def usb_charger_protect():
	m = ( box(x + xw*2, by+yw, bz+t + zw + upper_z).down(upper_z)
	 -box(bx, by, bz).right((x + xw*2-bx)/2).up(t)
	 -box(x, by+yw, t+upper_z).right(xw).down(upper_z)
	 -multitransform([translate(xw/2,(yw+by)/2,0), translate(x+xw*3/2,(yw+by)/2,0)])(cylinder(r=1.5, h=bz+zw+t+upper_z).down(upper_z))
	).translate(-(x + xw*2)/2, -(by+yw)/2 - y/2 + (by+s)/2, 0).rotateZ(gr(180))
	return m

def usb_charger_protect_hole():
	return multitransform([translate(xw/2,(yw+by)/2,0), translate(x+xw*3/2,(yw+by)/2,0)])(cylinder(r=1.5, h=bz+zw+t)).translate(-(x + xw*2)/2, -(by+yw)/2 - y/2 + (by+s)/2, -t/2).rotateZ(gr(180))


if __name__ == "__main__":
	#display(usb_charger() + usb_charger_protect().up(upper_z) + usb_plate_upper())
	display(usb_charger_protect())
	show()