#!/bin/sh
# アプリの自動起動を設定する
SCRIPT_DIR=`dirname $0`
cd $SCRIPT_DIR
echo "app auto start setting"
sudo cp autoStart_app.service /etc/systemd/system/
sudo systemctl enable autoStart_app.service
# sudo cp autoStart_julius.service /etc/systemd/system/
# sudo systemctl enable autoStart_julius.service
