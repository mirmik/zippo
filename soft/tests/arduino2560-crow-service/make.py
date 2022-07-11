#!/usr/bin/env python3
#coding: utf-8

import licant
from licant.cxx_modules import application
from licant.libs import include
from licant.modules import submodule

import time
import os

TOOLCHAIN = licant.gcc_toolchain("avr-")

include("igris")
include("zillot")
include("genos")
include("crow")
include("ralgo")
include("nos")

default_device = "/dev/ttyACM0"

remote_ip = "192.168.1.100"

@licant.routine(deps=["firmware.elf"])
def install(src="firmware.hex", tgt=default_device, *args):
	for cmd in [
		"avr-objcopy -O ihex -R .eeprom -R .fuse firmware.elf firmware.hex",
		f"avrdude -P{tgt} -v -cwiring -patmega2560 -b115200 -D -Uflash:w:./{src} -u"
	]:
		print(cmd)
		os.system(cmd)

@licant.routine
def terminal(path=default_device):
	os.system("gtkterm -p {} -s 115200 --parity none".format(path))


licant.cxx_application("firmware.elf",
	toolchain = TOOLCHAIN,
	sources=[
		"src/*.cpp"
	],
	mdepends=
	[
		"igris.std",
		"igris.posix",
		"igris.include",	
		"nos.include",	
		"ralgo.include",	

		"crow.minimal",
		("crow.allocator", "malloc"),		
		"nos.print",
		"nos.fprint",
		("nos.current_ostream", "nullptr"),

		"zillot",	
		"genos",

		"zillot.avr",
		"zillot.avr.atmega2560",	
		"zillot.arduino.mega",			
		"zillot.arduino.Adafruit_MotorShield",

		("igris.syslock", "irqs"),
		"igris.util",
		"igris.utilxx",
		"igris.cxx_support",
		("igris.systime", "jiffies"),
		("igris.dprint", "diag"),
		("crow.diagnostic", "stub"),
		("crow.select", "stub"),
		("igris.location", "stub")
	],

	include_paths = ["src"],
	defines=[
		"MEMORY_ECONOMY", 
		"WITHOUT_ATOF64=1", 
		"ADAFRUIT_MOTOR_SHIELD_NO_STEPPERS", 
		"ADAFRUIT_MOTOR_SHIELD_NO_PWM",
		"F_CPU=16000000",
		"NDEBUG"
	],

	cxx_flags = "-flto -ffunction-sections -fexceptions -fdata-sections -Wl,--gc-sections -Os -fno-rtti",
	cc_flags = "-flto -ffunction-sections -fdata-sections -Wl,--gc-sections -Os",
	ld_flags = "-flto -ffunction-sections -fdata-sections -Wl,--gc-sections -Os -fno-rtti",

	cxxstd = "c++17",
)

licant.ex("firmware.elf")
