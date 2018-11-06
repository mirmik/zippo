#!/usr/bin/python3
#coding: utf-8

import licant
from licant.cxx_modules import application
from licant.libs import include
from licant.cxx_make import make_gcc_binutils
from licant.modules import submodule

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
		("genos.board", "arduino_uno"),


		("genos.include"),
		
		("genos.irqtbl"),
		("genos.sched", "impl"),
		("gxx.syslock", "genos.atomic"),
		("genos.malloc", "lin"),

		("gxx.libc"),
		("gxx.std"),
		("gxx.posix"),
		("gxx.panic", "abort"),

		("gxx.include"),
		("gxx.util"),
		
		("gxx.diag", "impl"),
		("gxx.dprint", "diag"),
		("gxx.print", "dprint"),

		("crow"),
		("crow.allocator", "malloc"),

		("genos.mvfs"),
		("genos.systime"),
		submodule("genos.drivers.common"),
		submodule("genos.drivers.gpio.avr"), 
		submodule("genos.drivers.usart.avr"),

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
