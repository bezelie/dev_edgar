#!/bin/bash
echo "restart_app.sh start" >> debug.txt
date "+    %H:%M:%S" >> debug.txt
ps aux | grep python | grep -v grep | awk '{ print "kill -9", $2 }' | bash
ps aux | grep julius | grep -v grep | awk '{ print "kill -9", $2 }' | bash
echo "python and julius are killed" >> debug.txt
date "+    %H:%M:%S" >> debug.txt
/opt/bezelie/bin/boot_julius.sh
# ALSADEV="plughw:0,0" /usr/local/bin/julius -w /home/pi/bezelie/dev_edgar/chatEntity.dic -C /home/pi/bezelie/dev_edgar/julius.jconf -module &
echo "julius executed on back ground" >> debug.txt
date "+    %H:%M:%S" >> debug.txt
/opt/bezelie/bin/boot_python.sh
# cd /home/pi/bezelie/dev_edgar
# sleep 5
# /usr/bin/python /home/pi/bezelie/dev_edgar/demo_chat1.py
echo "demo_chat1.py executed" >> debug.txt
echo "restart_app.sh end" >> debug.txt
date "+    %H:%M:%S" >> debug.txt
echo "-------------------" >> debug.txt
exit 0
