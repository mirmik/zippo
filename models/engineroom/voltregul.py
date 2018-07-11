#!/usr/bin/env python3
#coding: utf-8

#MT3608

from zencad import *
from params import *

#)Размеры платы.
x=17.5
y=37.4
z=1.7

shift0=8
shift1=32

holder_x = 3
holder_t = 2
holder_z = 6

plate = box(x,y,z,center=True).up(z/2)

position_0 = translate(0, body_y/2 - x/2 - bottom_wall_thikness - shift0, bottom_wall_thikness) * rotateZ(deg(90))
position_1 = translate(0, body_y/2 - x/2 - bottom_wall_thikness - shift1, bottom_wall_thikness) * rotateZ(deg(90))

holder = union([
	box(holder_t, y + holder_t * 2, holder_z),
	box(holder_t + holder_x, holder_t, holder_z),
	box(holder_t + holder_x, holder_t, holder_z).forw(y + holder_t),
])

holder = holder.translate(-(holder_t * 2 + x) / 2, -(y + holder_t * 2) / 2, 0)
holder = holder + holder.mirrorYZ()


if __name__ == "__main__":
	display(holder + plate)
	show()