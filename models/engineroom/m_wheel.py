#!/usr/bin/python3
#coding: utf-8

from zencad import *
from params import *

def wheel():
	return cylinder(r=21, h=18.5, center=True).rotateY(gr(90))

def quadro_wheel():
	return sqrtrans()(wheel().translate(body_x/2 + 10.5, dist_between_whells/2, 5))

if __name__ == "__main__":
	display(quadro_wheel())
	show()