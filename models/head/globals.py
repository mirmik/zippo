from zencad import *

T=2
ROOF_R=40
SPIKE_N = 8
LIGHT_R = 6
LIGHT_HOLES = rotate_array(SPIKE_N)(cylinder(r=LIGHT_R, h=T).left(ROOF_R-LIGHT_R-T).rotateZ(deg(360/8/2)))
BORDER_T = 3

SPIKE_R1=3.5
SPIKE_R2 = ROOF_R - SPIKE_R1 - T

NUT_HOLE1 = rotate_array(4)((cylinder(r=1,h=T)+cone(r1=1,r2=2,h=T/2).up(T/2)).left(ROOF_R-T-2).rotateZ(deg(360/40)))
NUT_HOLE2 = rotate_array(4)((cylinder(r=1,h=T)).left(ROOF_R-T-2).rotateZ(deg(360/40)))

def motor_screw(r, h, f):
	c = cylinder(r, h)
	c -= halfspace().rotateX(deg(90)).moveY(f/2)
	c -= halfspace().rotateX(-deg(90)).moveY(-f/2)
	return c 

def cables_hole():
	t = T
	pnts = points([(18,0), (0,-11), (-18,0)])
	spine = interpolate(pnts)
	chole_width = 7
	tt = spine.d1(0)
	pt = tt.cross(vector(0,0,1)).normalize()
	perp = segment(point(pt*chole_width/2), point(-pt*chole_width/2))
	cables_hole = pipe(profile=perp.move(*pnts[0]), spine=spine) \
		+ circle(chole_width/2).move(*pnts[0]) + circle(chole_width/2).move(*pnts[-1])
	return cables_hole#.extrude(t) 

def stolb(r1,r2,r3,h1,angles=(deg(0),deg(90),deg(180),deg(270))):
	b = cylinder(r=r1,h=h1)
	tri = polygon([(0,0),(0,h1),(r3,0)])
	tri = tri.extrude(T, center=True)

	for d in angles:
		b = b + tri.rotateX(deg(90)).rotateZ(d)

	return (b 
		- cylinder(r=r2,h=h1)
	)

def stolb2(r1,r2,h1):
	b = cylinder(r=r1,h=h1)
	return (b 
		- cylinder(r=r2,h=h1)
	)
