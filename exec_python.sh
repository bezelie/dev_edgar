#!/bin/sh
# ps aux | grep python | grep -v grep | awk '{ print "sudo kill -9", $2 }' | sh
# sleep 1
# echo $!
cd /home/pi/bezelie/dev_edgar
python demo_chat1.py
exit 0
