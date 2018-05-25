#!/usr/bin/env python3
#coding: utf-8

from zencad import *
from params import *

#Переделка оригинальной стойки. Убрал скругление в изначальной модели

t = thickness

ssize = (5, t, miniservo_width + t)
shole_radius = miniservo_mount_radius
shole_up = t + miniservo_width / 2 

s = box(size = ssize) - cylinder(h=t, r=shole_radius).rotateX(gr(90)).up(shole_up).forw(t).right(ssize[0]/2)

m = (
	box(miniservo_length, miniservo_height, t) 
	+ s.right(miniservo_length - ssize[0])
	+ s
	+ box(t, miniservo_height, t).left(t)
	+ box(t, t, ssize[2]).left(t)
)


display(m)
show()