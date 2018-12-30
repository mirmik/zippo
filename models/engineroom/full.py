#!/usr/bin/env python3
#coding: utf-8

import zencad
from zencad import *

from evalcache import unlazy

zencad.enable_cache_diagnostic()

from bottom_full import bottom_full_scene
from bottom import z as bottom_z
from top import top_model
from top_assemble import top_assemble
from top import z2 as top_z
from control_body import z as control_z
from control_body import control_body

def engineroom_scene():
 	scene = Scene()
 	#scene.add(unlazy(top_model().up(bottom_z+top_z)), Color(0,1,0))
 	scene.append(top_assemble())#.up(bottom_z+top_z))
 	scene.add(unlazy(control_body().up(bottom_z+top_z+control_z)), Color(1,0,0))
 	scene.append(bottom_full_scene())
 	return scene

if __name__ == "__main__":
	show(engineroom_scene())