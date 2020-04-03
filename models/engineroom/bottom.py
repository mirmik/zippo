#!/usr/bin/env python3
#coding: utf-8

from zencad import *
from drive_place import drive_place
from usb_charger_plate import *
import params
from params import *

from m_accumholder import hole_x, hole_y, hole_d

import voltregul

#Габариты коробки
x = body_x
y = body_y
z = bottom_z

t = bottom_wall_thikness #Толщина стенок и дна.

dist_between_whells = params.dist_between_whells #Расстояния между осями колес.
sl = 17 #Ширина окна под двигатель.

#Ребро
stiffener = linear_extrude(polygon(points([ 
	(0,0), (z,0), (0,20)
])),(0,0,t),center=True).rotateY(deg(-90))

stiffener_long = linear_extrude(polygon(points([ 
	(0,0), (z,0), (0,30)
])),(0,0,t),center=True).rotateY(deg(-90))

#Расстановка рёбер.
stiffer_trans1 = multitransform([
	translate(+x/2,-dist_between_whells*3/16,0) * rotateZ(deg(90)),
	translate(-x/2,-dist_between_whells*3/16,0) * rotateZ(-deg(90)),
	translate(+x/2,dist_between_whells*3/16,0) * rotateZ(deg(90)),
	translate(-x/2,dist_between_whells*3/16,0) * rotateZ(-deg(90)),
])

stiffer_trans2 = multitransform([
	translate(-x/4,-y/2,0),
	translate(+x/4,-y/2,0),
	mirrorXZ() * translate(-x/4,-y/2,0),
	mirrorXZ() * translate(+x/4,-y/2,0),
])
#
#
m =  difference([
	linear_extrude(rectangle(x, y, center = True).fillet(5),(0,0,z)),
	linear_extrude(rectangle(x-2*t, y-2*t, center = True).fillet(5-t),(0,0,z-t)).up(t)
])

drive_place = drive_place(t,z,sl,t)

def bottom_model():
	return (m
		#Cylinders body
		+ sqrmirror() ( cylinder(r=5,h=z).translate(x/2-5,y/2-5,0)) 
	
		#Cylinders holes
		- sqrmirror()(cylinder(r=3,h=z).translate(x/2-5,y/2-5,0))
	
		#Drive places
		- sqrmirror()(drive_place.translate(x/2-t, dist_between_whells / 2, 0))

		#accumholder place
		- sqrmirror()(cylinder(r=hole_d/2, h=1000, center = True).translate(hole_x/2, hole_y/2, 0)).rotateZ(deg(90))

		#Добавляем ребра жесткости.
		+stiffer_trans1(stiffener)
		+stiffer_trans2(stiffener_long)

		+ usb_charger_position(usb_plate_upper())
		- usb_charger_position(usb_charger_port_hole()) #Отверстия под usb порт
		- usb_charger_position(usb_charger_protect_hole()).down(t) #Отверстие под держатель usb зарядника
		- on_position(on_hole()) #Отверстие под выключатель

		+ voltregul.position_0(voltregul.holder)
		+ voltregul.position_1(voltregul.holder)
	)

if __name__ == "__main__":
	display(bottom_model())
	show()