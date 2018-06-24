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
from m_wheel import quadro_wheel

bottom_full_arr = [ 
	bottom_model(), 
	accumholder_model().up(bottom_wall_thikness),
	quadro_wheel(),
	usb_charger_position(usb_charger()),
	usb_charger_position(usb_charger_protect()),
]

def bottom_full():
 	return union(bottom_full_arr)


if __name__ == "__main__":
	for d in bottom_full_arr: display(d)
	show()