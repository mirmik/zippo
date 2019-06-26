#!/usr/bin/env python3
#coding:utf-8

import licant 
import licant.libs
from licant.cxx_modules import application

licant.libs.include("igris")

licant.libs.include("nos")

licant.libs.include("ralgo")
licant.libs.include("malgo")

licant.libs.include("crow")
licant.libs.include("linalg-v3")

application("target",
	sources = ["main.cpp"],
	mdepends=["crow", "crow.udpgate", "ralgo", ("igris.ctrobj", "linux")],
	libs = ["pthread"],
)

licant.ex("target")