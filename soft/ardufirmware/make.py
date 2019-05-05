#!/usr/bin/python3
#coding: utf-8

import licant
from licant.cxx_modules import application
from licant.libs import include
from licant.cxx_make import make_gcc_binutils
from licant.modules import submodule

import time
import os

include("genos")
include("nos")
include("igris")
include("crow")
binutils = make_gcc_binutils("avr")

application("main", 
	binutils = binutils,
	sources = ["main.cpp"],
	target = "firmware.bin",

	mdepends = [
		#("genos.board", "arduino_mega"),
		("genos.board", "arduino_uno"),

		"genos.include",
		"genos.sched",

		"nos.include",
		("nos.current_ostream", "nullptr"),

		("igris.syslock", "genos.atomic"),
		"igris.libc",
		"igris.std",
		"igris.posix",

		("igris.dprint", "diag"),
		"igris.protocols.gstuff",

		("crow"),
		("crow.allocator", "pool"),
		#"crow.allocator",
		("crow.time", "genos"),

		"genos.drivers.avr",
		"genos.drivers.crow.uartgate",

		"genos.addons.adafruit_motor_shield",
	]
)

@licant.routine(deps=["main"])
def install():
	#os.system("avrdude -P/dev/ttyACM0 -v -cwiring -patmega2560 -b115200 -D -Uflash:w:./firmware.bin -u")
	os.system("avrdude -P/dev/ttyACM1 -v -carduino -patmega328p -b115200 -D -Uflash:w:./firmware.bin -u")

@licant.routine(deps=["main"])
def install_retrans():
	os.system("ctrans .12.127.0.0.1:10008 --pulse exit")
	os.system("avrdude -P/dev/ttyACM0 -v -carduino -patmega328p -b115200 -D -Uflash:w:./firmware.bin -u")
	time.sleep(1)
	os.system("bash /home/mirmik/start-trans.sh &")

remote_ip = "192.168.1.145"

@licant.routine(deps=['main'])
def remote_install():
	os.system("ctrans .12.{ip}:10008 --pulse exit".format(ip=remote_ip))
	os.system("scp ./firmware.bin mirmik@{ip}:/tmp/enginedrive.bin".format(ip=remote_ip))
	os.system("ssh mirmik@{ip} avrdude -P/dev/ttyACM0 -v -carduino -patmega328p -b115200 -D -Uflash:w:/tmp/enginedrive.bin -u".format(ip=remote_ip))
	time.sleep(1)
	os.system("ssh mirmik@{ip} ctrans --api --noconsole --udp 10008 --serial /dev/ttyACM0 > /dev/null &".format(ip=remote_ip))

@licant.routine
def terminal():
	os.system("sudo gtkterm -p /dev/ttyACM1 -s 115200")
	#os.system("sudo gtkterm -p /dev/ttyUSB0 -s 115200")

licant.ex("main")
