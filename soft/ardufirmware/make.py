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

#include("crow")
#include("malgo")
#include("linalg")

@licant.routine(deps=["firmware"])
def install_retrans():
	os.system("ctrans .12.127.0.0.1:10008 --pulse exit")
	os.system("avrdude -P/dev/ttyACM0 -v -carduino -patmega328p -b115200 -D -Uflash:w:./firmware.bin -u")
	time.sleep(1)
	os.system("bash /home/mirmik/start-trans.sh &")

remote_ip = "192.168.1.93"

@licant.routine(deps=['firmware'])
def remote_install():
	os.system("ctrans .12.{ip}:10010 --pulse exit".format(ip=remote_ip))
	os.system("scp ./firmware mirmik@{ip}:/tmp/enginedrive.bin".format(ip=remote_ip))
	os.system("ssh mirmik@{ip} avrdude -P/dev/ttyACM0 -v -carduino -patmega328p -b115200 -D -Uflash:w:/tmp/enginedrive.bin -u".format(ip=remote_ip))
	time.sleep(1)
	os.system("ssh mirmik@{ip} ctrans --api --noconsole --udp 10010 --serial /dev/ttyACM0 > /dev/null &".format(ip=remote_ip))

licant.cxx_application("firmware",
	toolchain = TOOLCHAIN,
	sources=["main.cpp"],
	mdepends=
	[
		"genos.include",	
		"igris.include",	
		"zillot.include",	
		"crow.include",	
		"nos.include",	
		"ralgo.include",	

#		"crow.address",
		"crow.minimal",
		"crow.protocol.pubsub",		
		("crow.allocator", "pool"),		
		"nos.print",
		"nos.fprint",
		("nos.current_ostream", "nullptr"),

		"genos",

		"zillot.chip.avr.atmega328p",	
		"zillot.arduino.uno",			
		"zillot.arduino.avr-systime",		
		"zillot.avr_i2c_device",
		"zillot.arduino.Adafruit_MotorShield",
		"zillot.drivers.serial.avr",

		("igris.syslock", "irqs"),
		"igris.util",
		"igris.ctrobj.common",
		"igris.utilxx",
		("igris.dprint", "stub"),
		"igris.compat.std",
		"igris.cxx_support",
	],

	cxx_flags = "-ffunction-sections -fdata-sections",
	cc_flags = "-ffunction-sections -fdata-sections",
	ld_flags = "-Wl,--gc-sections",

	cxxstd="c++17" 
)

licant.ex("firmware")
