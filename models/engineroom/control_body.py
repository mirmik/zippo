#!/usr/bin/python3
#coding: utf-8

from zencad import *
import params

x = params.body_x
y = params.body_y
t = params.bottom_wall_thikness

z = 35

platform_offset = 40

filrad = 5 #Радиус скругления

zh = 4

nhz = 3

nut_holder = linear_extrude(ngon(r=5.5,n=6),(0,0,nhz)) - linear_extrude(ngon(r=3.5,n=6),(0,0,nhz))

voltdisp = (26, 45)

base = rectangle(x, y, center = True).extrude(z).fillet(filrad,[0,1,2,4,5,6,8,9,10,12,13,14])

def b():
	bb = (
		difference([
			base,
			rectangle(x-2*t, y-2*t, center = True).extrude(z-t).fillet(filrad,[0,1,2,4,5,6,8,9,10,12,13,14]).up(t)
		])
	)
	return bb
			

def control_body():
	m = (
		#Основное тело
		b()

		#Колоны
		#- sqrtrans()(cylinder(r=5,h=z).translate(x/2-5,y/2-5,0)) 
		+ sqrtrans()(cylinder(r=5,h=z).translate(x/2-5,y/2-5,0))#.up(zh)
		
		#Отверстия в колоннах
		- sqrtrans()(cylinder(r=3,h=z).translate(x/2-5,y/2-5,0))

		#Отверстия под крепления поворотной платформы
		- sqrtrans()(cylinder(r=2,h=t).translate(24,24,0)).forw(platform_offset)
		- square(20).fillet(3,[0,1,2,3]).extrude(t).translate(-10,platform_offset-10,0)
	
		#Держатели гаек
		+ sqrtrans()(nut_holder.translate(24,24,0)).forw(platform_offset).up(t/2)

		- rectangle(20, 10, center = True).fillet(3,[0,1,2,3]).extrude(t)
		- rectangle(16, 8, center = True).fillet(3,[0,1,2,3]).extrude(t).right(40)
		- rectangle(16, 8, center = True).fillet(3,[0,1,2,3]).extrude(t).left(40)
		- rectangle(voltdisp[1], voltdisp[0], center = True).extrude(t).right(35).back(54)
	).mirrorXY()

	return m



if __name__ == "__main__":
	display(control_body())
	#display(b())
	show()