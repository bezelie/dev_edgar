#!/bin/bash
# DHCPサービスの起動
sleep 10
sudo /etc/init.d/isc-dhcp-server start &
# echo "starting startup applications"
exit 0
