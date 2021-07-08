#!/usr/bin/env python3

import licant
import licant.cxx_make

toolchain = licant.cxx_make.toolchain_gcc("avr-")

licant.include("igris")
licant.include("genos")

licant.cxx_application("firmware.elf",
	toolchain = toolchain,
	sources = ["main.cpp"],
	mdepends = [
		"igris.include",
		"genos.include",

		"igris.util",
		("igris.syslock", "genos.atomic"),
		("igris.dprint", "diag"),

		"cpu.avr.atmega328p",
		"genos.hal.avr",
		"genos.hal.avr.diag",

		"genos.sched2",
		"genos.systime",
		"genos.drivers.avr"
	],

	defines=["F_CPU=16000000"]
)

licant.objcopy(toolchain=toolchain, 
	src="firmware.elf", tgt="firmware.bin", format="binary", sections=[])

licant.ex("firmware.bin")