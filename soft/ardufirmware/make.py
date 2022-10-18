#!/usr/bin/env python3
#coding: utf-8

import licant
from licant.cxx_modules import application
from licant.libs import include
from licant.modules import submodule
import time
import os
import socket

TOOLCHAIN = licant.gcc_toolchain("avr-")

include("igris")
include("zillot")
include("genos")
include("crow")
include("ralgo")
include("nos")
default_device = "/dev/ttyACM0"

remote_ip = "192.168.1.100"


@licant.routine(deps=['firmware.elf'])
def remote_install():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((remote_ip, 5000))
    sock.send("stop transler\n".encode("utf-8"))
    os.system("ctrans .12.{ip}:10010 --pulse remote_exit".format(ip=remote_ip))
    os.system(
        "scp ./firmware.elf mirmik@{ip}:/tmp/enginedrive.bin".format(ip=remote_ip))
    os.system(
        "ssh mirmik@{ip} avrdude -P/dev/ttyACM0 -v -carduino -patmega328p -b115200 -D -Uflash:w:/tmp/enginedrive.bin -u".format(ip=remote_ip))
    time.sleep(1)
    os.system(
        "ssh mirmik@{ip} ctrans --api --noconsole --udp 10010 --serial /dev/ttyACM0 > /dev/null &".format(ip=remote_ip))
    sock.send("start transler\n".encode("utf-8"))
    sock.close()


@licant.routine(deps=["firmware.elf"])
def install(src="firmware.hex", tgt=default_device, *args):
    for cmd in [
            "avr-objcopy -O ihex -R .eeprom -R .fuse firmware.elf firmware.hex",
            f"avrdude -P{tgt} -v -carduino -patmega328p -b115200 -D -Uflash:w:./{src} -u"
    ]:
        print(cmd)
        os.system(cmd)


@licant.routine
def terminal(path=default_device):
    os.system("gtkterm -p {} -s 115200 --parity none".format(path))


licant.cxx_application("firmware.elf",
                       toolchain=TOOLCHAIN,
                       sources=[
                           "src/main.cpp",
                           "src/blink_task.cpp",
                           "src/motors.cpp",
                           "src/crow-service.cpp",
                           "src/command.cpp",
                       ],
                       mdepends=[
                           "igris.libc",
                           "igris.std",
                           "igris.posix",

                           # "genos.include",
                           "igris.include",
                           # "zillot.include",
                           # "crow.include",
                           "nos.include",
                           "ralgo.include",

                           #		"crow.address",
                           # "crow.minimal",
                           #("crow.allocator", "malloc"),
                           "nos.print",
                           "nos.fprint",
                           ("nos.current_ostream", "nullptr"),

                           "zillot",
                           "genos",

                           "zillot.avr",
                           "zillot.avr.atmega328p",
                           "zillot.arduino.uno",
                           #		"zillot.arduino.avr-systime",
                           #		"zillot.drivers.avr",
                           "zillot.arduino.Adafruit_MotorShield",
                           #		"zillot.drivers.serial.avr",

                           ("igris.syslock", "irqs"),
                           "igris.util",
                           "igris.utilxx",
                           "igris.cxx_support",
                           ("igris.systime", "jiffies"),
                           ("igris.dprint", "zillot.diag"),
                           #("crow.diagnostic", "stub"),
                           #("crow.select", "stub"),
                           ("igris.location", "stub"),
                           # "igris.printf_impl"
                           ("igris.printf_impl", "stub")
                       ],

                       include_paths=["src"],
                       defines=[
                           "MEMORY_ECONOMY",
                           "WITHOUT_ATOF64=1",
                           "ADAFRUIT_MOTOR_SHIELD_NO_STEPPERS",
                           "ADAFRUIT_MOTOR_SHIELD_NO_PWM",
                           "F_CPU=16000000",
                           "NDEBUG"
                       ],

                       cxx_flags="-flto -fmax-errors=3 -ffunction-sections -fexceptions -fdata-sections -Wl,--gc-sections -Os -fno-rtti",
                       cc_flags="-flto -ffunction-sections -fdata-sections -Wl,--gc-sections -Os",
                       ld_flags="-flto -ffunction-sections -fdata-sections -Wl,--gc-sections -Os -fno-rtti",

                       cxxstd="c++17",
                       )

licant.ex("firmware.elf")
