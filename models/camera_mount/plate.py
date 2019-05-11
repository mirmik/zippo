#!/usr/bin/env python3
#coding: utf-8

from zencad import *
from params import *

def l_vservo_mount():
	"""Переделка оригинальной стойки. Убрал скругление в изначальной модели"""
	t = thickness
	
	ssize = (5, t, miniservo_width + t)
	shole_radius = miniservo_mount_radius
	shole_up = t + miniservo_width / 2 
	
	s = box(size = ssize) - cylinder(h=t, r=shole_radius).rotateX(deg(90)).up(shole_up).forw(t).right(ssize[0]/2)
	
	m = (
		box(miniservo_length + 5 * 2, miniservo_height, t) 
		+ s.right(miniservo_length + 5)
		+ s
		+ box(t, miniservo_height, t).left(t)
		+ box(t, t, ssize[2]).left(t)
	).mirrorXZ()

	return m

def r_vservo_mount():
	cyl = (cylinder(r=miniservo_width/2, h=3, yaw=deg(180))
		.rotateY(deg(90)).rotateX(deg(90))
			.forw(miniservo_width/2)
				.up(miniservo_length+thickness-2)
	)
	ncyl = cylinder(r=3, h=8) 
	ncyl2 = cylinder(r=1, h=8)
	ncyl_trans = up(miniservo_length+thickness-2) * forw(miniservo_width/2) * right(thickness) * rotateY(deg(90))
	b = box(thickness, miniservo_width, miniservo_length+thickness-2)

	b2 = box(8 + thickness, thickness, miniservo_length+thickness-2).forw((miniservo_width - thickness)/2)
	b3 = box(2, thickness, miniservo_length+thickness-2.5-2).forw((miniservo_width - thickness)/2).right(8 + thickness - 2)
	b3 = b3.fillet(r=1.5, refs=[(9.152,5.163,25.000)])
	#hl(b3)

	return cyl + b + b2 - b3 + ncyl_trans(ncyl) - ncyl_trans(ncyl2)




def plate():
	D = 52
	base = cylinder(r=D/2, h=3)
	
	m = (
		base 
		- box(24, 12, 3, center = True).up(1.5).left(6)
		+ box(6, 12, 3, center = True).up(4.5).left(21)
		+ box(6, 12, 3, center = True).up(4.5).right(9)
		- cylinder(r =0.75, h = 6).right(8)
	
		- cylinder(r =0.75, h = 6).right(8-28)
	)

	return m

l_vmount = (l_vservo_mount().rotateY(deg(-90)).rotateZ(deg(90)).up(3)
	.forw(miniservo_width + miniservo_width / 2 + thickness)
	.left(miniservo_length-9)
)

r_vmount = r_vservo_mount().forw(miniservo_width/2).right(12)

#hl(r_vservo_mount())
display(plate() + l_vmount + r_vmount)
show()