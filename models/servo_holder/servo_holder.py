#!/usr/bin/env python3
#coding: utf-8

from zencad import *

servo_x = 23
servo_y = 13
servo_z = 18.5

ear_x  = 32
ear_y  = servo_y
ear_w  = 5

p1 = 3

t = 1

bot = linear_extrude(rectangle(servo_x, servo_z).fillet(2,(0,3)), t) #+ rectangle(ear_x, ear_y).fillet(2,(1,2)).left((ear_x - servo_x)/2)
ear = linear_extrude(rectangle(ear_w, servo_y + t).fillet(1, [1]), t)
ear = ear + ear.rotateX(gr(90)).forw(t)
bck = box(servo_x+2*t, t, servo_y + t).left(t)
hand = box(t,servo_z - p1,t)

body = union([
	bot,
	ear.translate(-ear_w,p1,0),
	ear.translate(-ear_w,p1,0).mirrorYZ().right(servo_x),
	bck.forw(servo_z),
	hand.up(servo_y).forw(p1).left(t),
	hand.up(servo_y).forw(p1).right(servo_x)
])

#display(bot)
display(body)
show()