#!/usr/bin/python3
#coding: utf-8

import zencad
from zencad import *

import evalcache
evalcache.enable()

from params import *
from bottom import bottom_model
from m_accumholder import accumholder_model
from usb_charger_plate import usb_charger, usb_charger_position, usb_charger_protect 
from usb_charger_plate import y as usb_charger_y
#from lipo_charger_protect import usb_protect
import m_wheel
import voltregul

bottom_full_arr = [ 
	bottom_model(), 
	accumholder_model().up(bottom_wall_thikness),
	m_wheel.quadro(),
	usb_charger_position(usb_charger()),
	usb_charger_position(usb_charger_protect()),
	voltregul.position_0(voltregul.plate),
	voltregul.position_1(voltregul.plate),
]

def bottom_full_scene():
	scene = Scene()

	scene.add(bottom_model().eval(), Color(0.6,0.8,0.6))
	scene.add(accumholder_model().up(bottom_wall_thikness).eval(), Color(1,1,1))
	scene.add(m_wheel.quadro().eval(), Color(1,1,1))
	scene.add(usb_charger_position(usb_charger()).eval(), Color(1,1,1))
	scene.add(usb_charger_position(usb_charger_protect()).eval(), Color(1,0,0))
	scene.add(voltregul.position_0(voltregul.plate).eval(), Color(1,1,1))
	scene.add(voltregul.position_1(voltregul.plate).eval(), Color(1,1,1))

	return scene


if __name__ == "__main__":
	show(bottom_full_scene())