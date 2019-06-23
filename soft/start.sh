start_after 1000 /home/mirmik/project/zippo/soft/wifi_starter.py &

start_after 1000 crowker --udp 10009 --tcp 10012 > /dev/null &
start_after 1500 ctrans --udp 10010 --serial /dev/ttyACM0 --api --noconsole > /dev/null &
start_after 1500 /home/mirmik/project/zippo/soft/videoovercrow/videoovercrow.py > /dev/null &
start_after 1500 /home/mirmik/project/zippo/soft/ahrs/target > /dev/null &
