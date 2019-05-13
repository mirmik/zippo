start_after 1000 crowker --udp 10009 > /dev/null &
start_after 1000 ctrans --udp 10010 --serial /dev/ttyACM0 --api --noconsole > /dev/null &
