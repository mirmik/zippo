sudo systemctl stop hostapd
sudo systemctl stop dnsmasq
sudo systemctl stop wpa_supplicant

sudo ifconfig wlan0 down
