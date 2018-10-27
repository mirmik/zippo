#!/usr/bin/python3
#coding: utf-8

import licant
from licant.cxx_modules import application
from licant.libs import include
from licant.cxx_make import make_gcc_binutils

import os

include("genos")
include("gxx")
include("crow")
binutils = make_gcc_binutils("avr")

application("main", 
	binutils = binutils,
	sources = ["main.cpp"],
	target = "firmware.bin",

	cxx_flags = "-Os -fpermissive -fno-threadsafe-statics -flto",
	cc_flags = "-Os -flto",

	include_modules = [
		("genos"),
		("genos.board", "arduino_uno"),

		
		("genos.irqtbl"),
		("genos.tasklet"),
		("genos.timer"),
		("genos.schedee"),
		("gxx.syslock", "genos.atomic"),
		("genos.malloc", "lin"),

		("genos.displace", "reset"),
		
		("gxx.libc"),
		("gxx.std"),
		("gxx.posix"),

		("gxx.include"),
		("gxx.util"),
#		("gxx.log2", "stub"),
		
		("gxx.diag", "impl"),
		("gxx.dprint", "diag"),
		("gxx.print", "dprint"),

		("gxx.panic", "abort"),

		("crow"),
		("crow.allocator", "malloc"),

		("genos.addons.adafruit_motor_shield")
	]
)

@licant.routine
def install():
	#os.system("sudo avrdude -P/dev/ttyACM0 -v -cwiring -patmega2560 -b115200 -D -Uflash:w:./firmware.bin -u")
	os.system("sudo avrdude -P/dev/ttyACM0 -v -carduino -patmega328p -b115200 -D -Uflash:w:./firmware.bin -u")

@licant.routine
def remote_install():
	os.system("ctrans .12.192.168.1.140:10008 --pulse 'exit' --type 15 --qos 2")
	os.system("scp ./firmware.bin mirmik@192.168.1.140:/tmp/enginedrive.bin")
	os.system("ssh mirmik@192.168.1.140 avrdude -P/dev/ttyACM0 -v -carduino -patmega328p -b115200 -D -Uflash:w:/tmp/enginedrive.bin -u")
	os.system("ssh mirmik@192.168.1.140 ctrans --api --udp 10008 --serial /dev/ttyACM0 > /dev/null &")

@licant.routine
def terminal():
	os.system("sudo gtkterm -p /dev/ttyACM0 -s 115200")

licant.ex(default = "main", colorwrap = True)
