#!/usr/bin/env python3
#coding:utf-8

import licant 
import licant.libs
from licant.cxx_modules import application

licant.libs.include("gxx")
licant.libs.include("crow")

application("target",
	sources = ["main.cpp"],
	include_modules = [
		("gxx", "posix"),
		("gxx.dprint", "cout"),
		("gxx.print", "cout"),

		("gxx.syslock", "mutex"),
		("gxx.inet", "posix"),

		("gxx.madgwick"),

		("crow"),
		("crow.udpgate"),
		("crow.allocator", "malloc"),
		("crow.time", "chrono"),
	],
	libs = ["pthread"],
)

licant.ex("target")