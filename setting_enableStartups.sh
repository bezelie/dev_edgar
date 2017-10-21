#!/bin/bash
# rc.localによってrc.startupsが自動起動するように設定する。
# rc.startupsはjulius, nodejs, pythonを実行する。
echo "app auto start setting"
cd /home/pi/bezelie/dev_edgar
sudo cp rc.startups /etc/rc.local
