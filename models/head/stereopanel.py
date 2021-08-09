#!/usr/bin/env python3
from zencad import *

eye_width = 130/2
	
left_eye_transform = left(eye_width / 2)
right_eye_transform = right(eye_width / 2)

# параметры платы камеры
bx = 25
by = 25
bz = 1.5

# параметры отверстий
hx = 21/2
hr = 1.2
hy1 = by/2 - (bx-hx*2)/2 -0.5
hy2 = hy1 - 12


def plate(h):
	d = 4
	x = eye_width + bx + d/2
	y = by + d/2
	z = h
	
	ex = 9
	ey = 9
	
	
	def eye():
		return ( 
			move(0,hy2)(box(ex, ey, z, center=True)) 
			+ multitrans([
				move(+hx, hy1),
				move(-hx, hy1),
				move(+hx, hy2),
				move(-hx, hy2)
			])(cylinder(hr, z, center=True))
		)
	
	m = (
		rectangle(x,y, center=True).extrude(z,center=True)
		#- rectangle(x-d/2,y-d/2, center=True).fillet2d(1).extrude(z-d/4,center=True).up(d/8)
		- left_eye_transform(eye())
		- right_eye_transform(eye())
	)
	
	return m

def camera():
	m = (
		rectangle(bx,by,center=True).fillet2d(1).extrude(bz, center=True)
		- multitrans([
			move(+hx, hy1),
			move(-hx, hy1),
			move(+hx, hy2),
			move(-hx, hy2)
		])(cylinder(hr, bz, center=True))
	)

	return m
