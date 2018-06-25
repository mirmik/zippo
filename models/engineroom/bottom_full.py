#!/usr/bin/python3
#coding: utf-8

import zencad
from zencad import *

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

def bottom_full():
 	return union(bottom_full_arr)


if __name__ == "__main__":
	for d in bottom_full_arr: display(d)
	show()