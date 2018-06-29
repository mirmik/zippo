#!/usr/bin/python3
#coding: utf-8

import zencad
from zencad import *

import evalcache
evalcache.enable()

from bottom_full import bottom_full_scene
from bottom import z as bottom_z
from top import top_model
from top import z2 as top_z

def engineroom_scene():
 	scene = Scene()
 	scene.add(top_model().up(bottom_z+top_z).eval(), Color(0,1,0))
 	scene.append(bottom_full_scene())
 	return scene

if __name__ == "__main__":
	show(engineroom_scene())