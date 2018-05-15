from zencad import *

sqtrans = multitransform([
	translate(0,0,0),
	mirrorYZ(),
	mirrorXZ(),
	mirrorZ(),
])