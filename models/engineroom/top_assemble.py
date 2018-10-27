#!/usr/bin/env python3
#coding: utf-8

import zencad
from zencad import *

from top import top_model, ardu_position, rasp_position
from ardubase import ardubox
from raspbase import raspbox

def top_assemble():
 	scene = Scene()
 	scene.add(top_model().eval(), Color(0,1,0))
 	scene.add(ardu_position(ardubox()).eval(), Color(0.6,0.6,0.8))
 	scene.add(rasp_position(raspbox()).eval(), Color(0.6,0.6,0.8))
 	return scene

if __name__ == "__main__":
	show(top_assemble())