#!/bin/sh
# ps aux | grep python | grep -v grep | awk '{ print "kill -9", $2 }' | sh
cd /home/pi/bezelie/dev_edgar
python demo_chat1.py
exit 0
