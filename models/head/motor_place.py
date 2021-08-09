#!/usr/bin/env python3

from zencad import *

H = 2

m = cylinder(r=28/2,h=H)
m -= cylinder(r=5.2, h=H).movY(8)
m += cylinder(r=4,h=H).movX(35/2)
m += cylinder(r=4,h=H).movX(-35/2)
m += box(5,4*2,H,center=True).up(H/2).movX(15)
m += box(5,4*2,H,center=True).up(H/2).movX(-15)
m -= cylinder(r=2.5,h=H).movX(35/2)
m -= cylinder(r=2.5,h=H).movX(-35/2)

to_stl(m, "/home/mirmik/models/holder.stl", delta=0.1)

disp(m)
show()