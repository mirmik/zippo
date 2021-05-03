#!/usr/bin/env python3
#coding: utf-8

import licant
from licant.cxx_modules import application
from licant.libs import include
from licant.cxx_make import make_gcc_binutils
from licant.modules import submodule

import time
import os

TOOLCHAIN = make_gcc_binutils("avr")

include("genos")
include("nos")
include("igris")
include("crow")
include("ralgo")
include("malgo")
include("linalg")

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
	mdepends=[	
		"crow.minimal",
		("crow.protocol.pubsub"),
		("crow.allocator", "pool"),
		("crow.time", "genos"),

		"genos.drivers.crow.uartgate",
		"genos.addons.adafruit_motor_shield",

		"igris.protocols.gstuff",

		("igris.dprint", "stub"),
		("genos.diag", "stub"),
		"genos.sched",

		"igris.compat.std",
		"igris.compat.posix",

		"nos",

		"ralgo",
		("ralgo.disctime", "manual"),
		"malgo",
		"linalg",

		"genos.arduino_compat",
		"genos",

		"board.arduino_mega",
		"cpu.avr.atmega2560"
		#"genos.drivers.avr"

	],
	defines=["WITHOUT_LOG2=1"],
)

licant.ex("firmware")
