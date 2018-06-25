#!/usr/bin/python3
#coding: utf-8

import zencad
from zencad import *

from bottom_full import bottom_full
from bottom import z as bottom_z
from top import top_model
from top import z2 as top_z

def engineroom():
 	scene = Scene()
 	scene.add(top_model().up(bottom_z+top_z), Color(0,1,0))
 	scene.append(bottom_full())
 	return scene

if __name__ == "__main__":
	show(engineroom())