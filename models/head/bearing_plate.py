#!/usr/bin/env python3

from zencad import *
from globals import *

from room2 import Room

class RotationPlate(zencad.assemble.unit):
	def __init__(self):
		super().__init__()

		self.x = Room().x - 2*T
		self.y = Room().y - 2*T
		
		self.add(self.model())
		
		
	def model(self):
		X = 98
		Y = 96
		Z = 3

		# Заготовка
		m = box(X, Y, Z, center=True).moveZ(Z/2)

		# Строим внешний цилиндр
		CZ = 5+Z
		m += cylinder(r=43, h=CZ) - cylinder(r=40, h=CZ)

		# Вырезаем центральное отверстие
		m -= cylinder(r=5, h=Z)

		# Вырезаем сквозные отверстия под винты на стороне нижней крышки.
		m -= rotate_array(8)(cylinder(r=5, h=Z).moveY(32)).rotZ(deg(360)/16)

		# Вырезаем отверстия под винты для крепления платы.
		m -= sqrmirror()(cylinder(r=2,h=Z).move(X/2-3, Y/2-3, 0))

		# Вырезаем полость под провода.
		S = 4
		F = 8
		M= point3(-15,-5)
		s = cylinder(r=S,h=Z).move(*M)
		p0 = point3(S, 0, 0).rotZ(deg(45)).move(*M)
		p1 = point3(S, 0, 0).rotZ(-deg(135)).move(*M)
		w1 = interpolate([p0,point3(0,-F,0),p0.mirrorYZ()])
		w2 = interpolate([p1,point3(0,-F-S*2,0),p1.mirrorYZ()])
		r = ruled(w1,w2)

		hole = s + s.mirrorYZ() + r.extrude(Z)

		m -= hole 

		# Строим точечные опоры
		m += rotate_array(8)((sphere(r=4)-halfspace()).moveX(35)).moveZ(Z)

		# Скругляем полость для проводов
		m = fillet(m, refs=[
			point3(0,-F-S*2, 0),
			point3(0,-F-S*2, Z)
		], r=1)
		return m

if __name__ == "__main__":
	rotplate = RotationPlate()
	disp(rotplate)
	to_stl(rotplate.model(), "bearing-plate.stl", delta=0.1)
	show()