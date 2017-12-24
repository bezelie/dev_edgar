#!/bin/bash
ps aux | grep julius | grep -v grep | awk '{ print "kill -9", $2 }' | sh
ps aux | grep python | grep -v grep | awk '{ print "kill -9", $2 }' | sh
ALSADEV="plughw:0,0" julius -w chatEntity.dic -C julius.jconf -module > /dev/null &
echo "Julius's Process ID = "$!
sleep 10
echo "10 seconds passed"
# cd /home/pi/bezelie/dev_edgar
python /home/pi/bezelie/dev_edgar/demo_chat1.py &
# python sample_record1.py
exit 0
