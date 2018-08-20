#!/usr/bin/python3
#coding:utf-8

from zencad import *

#Размеры платы.
plate_x = 56
plate_y = 85
plate_z = 1

#толщина стенок
t = 1.5

#Внутренний размер коробки.
in_x = plate_x + 1
in_y = plate_y + 1

#Габаритные размеры
x = in_x + 2 * t
y = in_y + 2 * t
z = 5

hole_coords = [
	(3.5, 3.5),
	(plate_x - 3.5, 3.5),
	(3.5, 3.5 + 58),
	(plate_x - 3.5, 3.5 + 58),
]

#размер уха.
s = 8

hsys = translate(t+0.5,t+0.5,0)
hsysm = multitransform([translate(t[0], t[1], 0) * hsys for t in hole_coords])
ear_place = multitransform([
	translate(x+s/2,s/2,0),
	#right(x+s),
	translate(s/2, y+s/2,0),
	translate(x-s/2, y+s/2, 0),
])

ear = box(s,s,t, center=True).up(t/2) - cylinder(h=t, r=1.6)

def raspbox():
	m = (
		box(x,y,z) - box(in_x, in_y, z - t).translate(t,t,t) 

		#стойки
		+ hsysm(cylinder(h=5, r=3)) - hsysm(cylinder(h=5-t, r=1.45)).up(t)

		#отверстия под карту
		- box(13, t, z).right(x/2 - 13/2).forw(y-t)

		+ ear_place(ear)


	)#.translate(-s/2,s/2,0)
	return m



if __name__ == "__main__":
	display(raspbox())
	show()