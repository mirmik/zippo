#!/usr/bin/python3
#coding: utf-8

import zencad
from zencad import *

from evalcache import unlazy

from params import *
from bottom import bottom_model
from m_accumholder import accumholder_model
from usb_charger_plate import usb_charger, usb_charger_position, usb_charger_protect 
from usb_charger_plate import y as usb_charger_y
from usb_charger_plate import upper_z as usb_charger_upper
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

	scene.add(unlazy(bottom_model()), Color(0.6,0.8,0.6))
	scene.add(unlazy(accumholder_model().up(bottom_wall_thikness)), Color(1,1,1))
	scene.add(unlazy(m_wheel.quadro()), Color(1,1,1))
	scene.add(unlazy(usb_charger_position(usb_charger())), Color(1,1,1))
	scene.add(unlazy(usb_charger_position(usb_charger_protect().up(usb_charger_upper))), Color(1,0,0))
	scene.add(unlazy(voltregul.position_0(voltregul.plate)), Color(1,1,1))
	scene.add(unlazy(voltregul.position_1(voltregul.plate)), Color(1,1,1))

	return scene


if __name__ == "__main__":
	show(bottom_full_scene())