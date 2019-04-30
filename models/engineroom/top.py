#!/usr/bin/env python3
#coding: utf-8

from zencad import *
import params

import ardubase
import raspbase

x = params.body_x
y = params.body_y
t = params.bottom_wall_thikness

z2 = 15

wires_path_hole = box(5,10,t)
wires_path_hole_trans = (35,20,0)

ardu_position = back(25) * right(10)
rasp_position = translate(-params.body_x/2 + t +1,-params.body_y/2 + 5*2 + 0.5,0)#back(36) * left(59)

def top_model():
	m = (
		#Основное тело
		difference([
			linear_extrude(rectangle(x, y, center = True).fillet(5),(0,0,z2)),
			linear_extrude(rectangle(x-2*t, y-2*t, center = True).fillet(5-t),(0,0,z2-t)).up(t)
		])
	
		#Колоны
		+ sqrtrans()(cylinder(r=5,h=z2).translate(x/2-5,y/2-5,0)) 
		
		#Отверстия в колоннах
		- sqrtrans()(cylinder(r=3,h=z2).translate(x/2-5,y/2-5,0))
	
		#Для проводов
		#- sqrtrans()(wires_path_hole.translate(*wires_path_hole_trans)).back(30)
		#- sqrtrans()(wires_path_hole.right(10).translate(*wires_path_hole_trans)).back(30)
		#- sqrtrans()(wires_path_hole.right(20).translate(*wires_path_hole_trans)).back(30)
		- box(40,45,t, center=True).up(t/2).translate(-37.5,45,0)
		- box(30,20,t, center=True).up(t/2).translate(34,65,0)
		- box(45,40,t, center=True).up(t/2).translate(34,-53,0)
		#- box(45,38,t, center=True).up(t/2).back(45).right(33)

		-ardu_position( ardubase.ear_place(cylinder(r=2, h=t)) )
		-rasp_position( raspbase.ear_place(cylinder(r=2, h=t)) )

	).mirrorXY()
	return m

if __name__ == "__main__":
	display(top_model())
	show()