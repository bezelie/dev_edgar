#!/bin/bash
# pythonスクリプト起動スクリプト
sleep 1 # 自動起動に失敗する場合、この待ち時間を長くしてみてください
cd /home/pi/bezelie/dev_edgar
python demo_theater.py
exit 0
