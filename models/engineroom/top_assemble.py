#!/usr/bin/env python3
#coding: utf-8

import zencad
from zencad import *

from top import top_model, ardu_position, rasp_position
from ardubase import ardubox
from raspbase import raspbox

from bottom import z as bottom_z
from top import z2 as top_z
from control_body import z as control_z

top_position = up(bottom_z+top_z)

def top_assemble():
 	scene = Scene()
 	scene.add(top_position(top_model()).unlazy(), Color(0,1,0))
 	scene.add(top_position(ardu_position(ardubox())).unlazy(), Color(0.6,0.6,0.8))
 	scene.add(top_position(rasp_position(raspbox())).unlazy(), Color(0.6,0.6,0.8))
 	return scene

if __name__ == "__main__":
	show(top_assemble())