#!/bin/bash
# 顔認識モードpythonスクリプト起動スクリプト
sleep 1 # 自動起動に失敗する場合、この待ち時間を長くしてみてください
cd /home/pi/bezelie/dev_edgar
/usr/bin/python /home/pi/bezelie/dev_edgar/demo_rangeCamera1.py
exit 0
