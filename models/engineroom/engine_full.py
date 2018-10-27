#!/usr/bin/env python3
#coding: utf-8

import zencad
from zencad import *

from bottom_full import bottom_full_scene
from bottom import z as bottom_z
from top import top_model
from top import z2 as top_z
from control_body import z as control_z
from control_body import control_body

def engineroom_scene():
 	scene = Scene()
 	scene.add(top_model().up(bottom_z+top_z).unlazy(), Color(0,1,0))
 	#scene.add(control_body().up(bottom_z+top_z+control_z).eval(), Color(1,0,0))
 	scene.append(bottom_full_scene())
 	return scene

if __name__ == "__main__":
	show(engineroom_scene())