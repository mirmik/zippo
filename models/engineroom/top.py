#!/usr/bin/env python3
#coding: utf-8

from zencad import *
from utils import sqtrans
import params

x = params.body_x
y = params.body_y
t = params.bottom_wall_thikness

z2 = 10
nhz = 3

nut_holder = linear_extrude(ngon(r=5,n=6),(0,0,nhz)) - linear_extrude(ngon(r=3,n=6),(0,0,nhz))

m = (
	#Основное тело
	difference([
		linear_extrude(rectangle(x, y, center = True).fillet(5,[0,1,2,3]),(0,0,z2)),
		linear_extrude(rectangle(x-2*t, y-2*t, center = True).fillet(5-t,[0,1,2,3]),(0,0,z2-t)).up(t)
	])

	#Колоны
	+ sqtrans(cylinder(r=5,h=z2).translate(x/2-5,y/2-5,0)) 
	
	#Отверстия в колоннах
	- sqtrans(cylinder(r=3,h=z2).translate(x/2-5,y/2-5,0))
	
	#Отверстия под крепления поворотной платформы
	- sqtrans(cylinder(r=1,h=t).translate(24,24,0)).forw(30)

	#Держатели гаек
	+ sqtrans(nut_holder.translate(24,24,0)).forw(30).up(t/2)

	#Для проводов
	- cylinder(r = 10, h = t).back(20)
)

display(m)
show()