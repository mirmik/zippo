#!/usr/bin/env python3

import os

MODE = "wpa"

os.system("ifconfig wlan0 up")

if MODE == "wpa":
	os.system("wpa_supplicant -Dnl80211 -iwlan0 -c/etc/wpa_supplicant/wpa_supplicant.conf > /dev/null &")

elif MODE == "ap":
	os.system("systrmctl start hostapd")
	os.systam("systemctl start dnsmasq")
