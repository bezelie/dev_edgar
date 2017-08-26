# アプリの自動起動を無効化する
#!/bin/sh
SCRIPT_DIR=`dirname $0`
cd $SCRIPT_DIR
echo "disable auto start"
sudo systemctl disable autoStart_app.service
# sudo systemctl disable autoStart_julius.service
