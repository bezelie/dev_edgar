#!/bin/bash
# DHCPサービスの起動
sleep 10s
sudo /etc/init.d/isc-dhcp-server start &
# /usr/local/nodejs/bin/node /home/pi/bezelie/dev_edgar/server_editChat.js &
# echo "starting startup applications"
exit 0
