#!/usr/bin/env python3
#coding: utf-8

from zencad import *

usb_y = 5
usb_x = 7.2
usb_z = 2.6

plate_x =12.2
plate_z = 1

xw = 5
yw = 2
zw = 1

b = box(plate_x + xw*2, usb_y+yw, usb_z+plate_z + zw)
u = box(usb_x, usb_y, usb_z).right((plate_x + xw*2-usb_x)/2).up(plate_z)
p = box(plate_x, usb_y+yw, plate_z).right(xw)
c = multitransform([translate(xw/2,(yw+usb_y)/2,0), translate(plate_x+xw*3/2,(yw+usb_y)/2,0)])(cylinder(r=1.5, h=usb_z+zw+plate_z))

display(b-u-p-c)
show()
