#! /bin/sh
# node server
# node /home/pi/bezelie/dev_edgar/server_editChat.js &
echo "starting startup applications"
sleep 5
# DHCPサービスの起動
sudo service isc-dhcp-server start
# applications起動
sleep 20
cd /home/pi/bezelie/dev_edgar
sh exec_juliusChat.sh
sleep 3
python demo_chat1.py
exit 0
