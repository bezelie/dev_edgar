#!/usr/bin/python
# -*- coding: utf-8 -*-
#
import cv2
import module_theater
from time import sleep
import subprocess                  # 外部プロセスを実行するモジュール
import json                        # jsonファイルを扱うモジュール
import RPi.GPIO as GPIO            # GPIO(汎用入出力端子)ライブラリの読み込$
import re                          # 正規表現モジュール

# CONST
demoMode = "on"
talkWait = 0.2
PINK   = 1
BLUE   = 2
RED    = 3
YELLOW = 4
GREEN  = 5

# 変数
scenarioFile = "/home/pi/bezelie/dev_edgar/theater.json"        # 設定ファイル

# Setting
GPIO.setmode(GPIO.BCM)                 # GPIOをGPIO番号で指定できるように設定
GPIO.setup(17, GPIO.IN)                # GPIOのピンを入力モードに設定
GPIO.setup(27, GPIO.IN)                # GPIOのピンを入力モードに設定
GPIO.setup(22, GPIO.IN)                # GPIOのピンを入力モードに設定
GPIO.setup(23, GPIO.IN)                # GPIOのピンを入力モードに設定
GPIO.setup(24, GPIO.IN)                # GPIOのピンを入力モードに設定
bez = module_theater.Control()         # べゼリー操作インスタンスの生成
sleep(0.5)

# メインループ
def main():
  try:
    print "開始します"
    f = open (scenarioFile,'r')
    data = json.load(f)
    sce = 0
    scene = 'scene0'
    i = 0
    while True:
      if data[scene][i]['kind'] == 'title':
#        sleep (1)
        bez.dispText(0, sce, i)  # Text
#        sleep (1)
        subprocess.call("aplay /home/pi/bezelie/dev_edgar/pafu1.wav", shell=True)
        sleep (1)
        cv2.destroyAllWindows()
#        sleep (1)
        i = i+1
      elif data[scene][i]['kind'] == 'end':
        bez.dispText(0, sce, i)  # Text
        subprocess.call("aplay /home/pi/bezelie/dev_edgar/lauph1.wav", shell=True)
        sleep (1)
        cv2.destroyAllWindows()
        sleep (1)
        sce = 0
        scene = 'scene0'
        i = 0
      elif data[scene][i]['kind'] == 'speech':
        # data input
        if data[scene][i]['name'] == 'PINK': id = 1
        if data[scene][i]['name'] == 'BLUE': id = 2
        if data[scene][i]['name'] == 'RED': id = 3
        if data[scene][i]['name'] == 'YELLOW': id = 4
        if data[scene][i]['name'] == 'GREEN': id = 5
        text = data[scene][i]['word']
        voice = re.sub('\n','',text)
        if text <> "":
          bez.speech(id, sce, i)                # Voice
          bez.dispText(id, sce, i)  # Text
        action = data[scene][i]['action']
        bez.act(id, action)                  # Action
        wait = (len(voice)*talkWait)+float(data[scene][i]['wait'])
        print wait
        sleep (wait)
        bez.stop()
        cv2.destroyAllWindows()
        i = i+1

      elif data[scene][i]['kind'] == 'select':
        counter = 0
        bez.moveCenter()                     # サーボをセンタリング
        bez.dispText(0, sce, 0)  # Text
        bez.dispText(PINK, sce, 1)  # Text
        bez.dispText(BLUE, sce, 2)  # Text
        bez.dispText(RED, sce, 3)  # Text
        bez.dispText(YELLOW, sce, 4)  # Text
        bez.dispText(GREEN, sce, 5)  # Text
        subprocess.call("aplay /home/pi/bezelie/dev_edgar/question1.wav", shell=True)

        while True:                        # 繰り返し処理
          if GPIO.input(17)==GPIO.HIGH:    # 
            scene = data[scene][i]['target1']
            sce = int(re.sub('scene','',scene))
            print "PINKスイッチが押されています"
            break
          elif GPIO.input(27)==GPIO.HIGH:    # 
            scene = data[scene][i]['target2']
            sce = int(re.sub('scene','',scene))
            print "BLUEスイッチが押されています"
            break
          elif GPIO.input(22)==GPIO.HIGH:    # 
            scene = data[scene][i]['target3']
            sce = int(re.sub('scene','',scene))
            print "REDスイッチが押されています"
            break
          elif GPIO.input(23)==GPIO.HIGH:    # 
            scene = data[scene][i]['target4']
            sce = int(re.sub('scene','',scene))
            print "YELLOWスイッチが押されています"
            break
          elif GPIO.input(24)==GPIO.HIGH:    # 
            scene = data[scene][i]['target5']
            sce = int(re.sub('scene','',scene))
            print "GREENスイッチが押されています"
            break
          else:                            # 
            # print "スイッチは押されてません"
            sleep (0.1)                      # 0.5秒待つ
            counter = counter + 1
            if counter > 100:
              scene = data[scene][i]['target5']
              sce = int(re.sub('scene','',scene))
              break

        counter = 0
        subprocess.call("aplay /home/pi/bezelie/dev_edgar/switch1.wav", shell=True)
        cv2.destroyAllWindows()
        i = 0
        sleep (1)
      else:
        print "Not Matched"
  except KeyboardInterrupt:
    print ' 終了しました'

if __name__ == "__main__":
    main()
