#!/usr/bin/python3
#coding: utf-8

import zencad
from zencad import *

from bottom_full import bottom_full
from bottom import z as bottom_z
from top import top_model
from top import z2 as top_z

def full():
 	return union([ 
		bottom_full(), 
		top_model().up(bottom_z+top_z),
 	])


if __name__ == "__main__":
	display(full())
	show()