#!/usr/bin/env python3
#coding:utf-8

import licant 
import licant.libs
from licant.cxx_modules import application

licant.libs.include("gxx")
licant.libs.include("crow")

application("target",
	sources = ["main.cpp"],
	mdepends=["crow", "crow.udpgate", "gxx", "gxx.madgwick"],
	libs = ["pthread"],
)

licant.ex("target")