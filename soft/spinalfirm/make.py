#!/usr/bin/env python3

import licant

licant.include("ralgo")
licant.include("igris")
licant.include("nos")
licant.include("crow")

licant.cxx_application("simulator",
	sources=[
		"simulator_main.cpp",
		"motor_shield.cpp"
	],
	mdepends=["ralgo", "igris", "nos"]
)

licant.ex("simulator")