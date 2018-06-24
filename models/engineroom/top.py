#!/usr/bin/env python3
#coding: utf-8

from zencad import *
import params

x = params.body_x
y = params.body_y
t = params.bottom_wall_thikness

z2 = 15
nhz = 3

platform_offset = 40

nut_holder = linear_extrude(ngon(r=5.5,n=6),(0,0,nhz)) - linear_extrude(ngon(r=4,n=6),(0,0,nhz))
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
		
		#Отверстия под крепления поворотной платформы
		- sqrtrans()(cylinder(r=1.5,h=t).translate(24,24,0)).forw(platform_offset)
		- box(20,20,t).translate(-10,platform_offset-10,0)
	
		#Держатели гаек
		+ sqrtrans()(nut_holder.translate(24,24,0)).forw(platform_offset).up(t/2)
	
		#Для проводов
		- sqrtrans()(wires_path_hole.translate(*wires_path_hole_trans)).back(30)
	).mirrorXY()
	return m

if __name__ == "__main__":
	display(top_model())
	show()