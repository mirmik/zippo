mkdir -p /etc/rfdaemon

sudo systemctl stop rfdaemon.service
cp rfdaemon-applicatons.json /etc/rfdaemon/applications.json
cp reproxy.yml /home/mirmik/.reproxy.yml
sudo systemctl start rfdaemon.service