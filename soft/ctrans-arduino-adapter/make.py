#!/usr/bin/env python3
import licant

licant.cxx_application("ctrans-arduino-adapter",
	sources = ["main.cpp"],
	libs = ["nos", "igris", "crow", "pthread"]
)

licant.ex("ctrans-arduino-adapter")