#!/usr/bin/env python3
#coding: utf-8

from zencad import *
import params

x = params.body_x
y = params.body_y
t = params.bottom_wall_thikness

z2 = 15

wires_path_hole = box(5,10,t)
wires_path_hole_trans = (35,20,0)

def top_model():
	m = (
		#Основное тело
		difference([
			linear_extrude(rectangle(x, y, center = True).fillet(5,[0,1,2,3]),(0,0,z2)),
			linear_extrude(rectangle(x-2*t, y-2*t, center = True).fillet(5-t,[0,1,2,3]),(0,0,z2-t)).up(t)
		])
	
		#Колоны
		+ sqrtrans()(cylinder(r=5,h=z2).translate(x/2-5,y/2-5,0)) 
		
		#Отверстия в колоннах
		- sqrtrans()(cylinder(r=3,h=z2).translate(x/2-5,y/2-5,0))
	
		#Для проводов
		- sqrtrans()(wires_path_hole.translate(*wires_path_hole_trans)).back(30)
		- sqrtrans()(wires_path_hole.right(10).translate(*wires_path_hole_trans)).back(30)
		- sqrtrans()(wires_path_hole.right(20).translate(*wires_path_hole_trans)).back(30)
	).mirrorXY()
	return m

if __name__ == "__main__":
	display(top_model())
	show()