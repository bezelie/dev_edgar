#!/bin/sh
# ps aux | grep python | grep -v grep | awk '{ print "kill -9", $2 }' | sh
cd /home/pi/bezelie/dev_edgar
python sample_servo1.py
exit 0
