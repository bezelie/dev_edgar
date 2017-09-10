# アプリの自動起動をkaijoする
#!/bin/bash
echo "app auto start setting"
cd /home/pi/bezelie/dev_edgar
sudo cp rc.startups /etc/rc.local
