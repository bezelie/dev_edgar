# アプリの自動起動をkaijoする
#!/bin/sh
echo "app auto start cancelling"
cd /home/pi/bezelie/dev_edgar
sudo cp rc.nothing /etc/rc.local
