#!/usr/bin/python
# -*- coding: utf-8 -*-
#
import cv2
import flitz
from time import sleep
import subprocess                     # 外部プロセスを実行するモジュール
import json                        # jsonファイルを扱うモジュール
import RPi.GPIO as GPIO                # GPIO(汎用入出力端子)ライブラリの読み込$
import re                          # 正規表現モジュール

# CONST
PINK = 1
BLUE = 2
RED = 3
YELLOW = 4
GREEN = 5

# 変数
scenarioFile = "/home/pi/bezelie/dev_edgar/scenario.json"        # 設定ファイル

# Setting
GPIO.setmode(GPIO.BCM)                 # GPIOをGPIO番号で指定できるように設定
GPIO.setup(17, GPIO.IN)                # GPIOのピンを入力モードに設定
GPIO.setup(27, GPIO.IN)                # GPIOのピンを入力モードに設定
GPIO.setup(22, GPIO.IN)                # GPIOのピンを入力モードに設定
GPIO.setup(23, GPIO.IN)                # GPIOのピンを入力モードに設定
GPIO.setup(24, GPIO.IN)                # GPIOのピンを入力モードに設定
bez = flitz.Control()               # べゼリー操作インスタンスの生成
bez.moveCenter()                     # サーボをセンタリング
sleep(0.5)

# メインループ
def main():
  try:
    print "開始します"
    f = open (scenarioFile,'r')
    data = json.load(f)
    i = 0
    scene = 'scene0'
    while True:
      if data[scene][i]['kind'] == 'title':
        text = data[scene][i]['word']
        size = 64
        align = 'center'
        bez.dispText(0, text, size, align)  # Text
        subprocess.call("aplay shocked.wav", shell=True)
        cv2.destroyAllWindows()
        sleep (1)
        i = i+1
      elif data[scene][i]['kind'] == 'end':
        scene = 'scene0'
        text = 'The End'
        size = 64
        align = 'center'
        bez.dispText(0, text, size, align)  # Text
        subprocess.call("aplay end.wav", shell=True)
        cv2.destroyAllWindows()
        sleep (1)
        i = 0
      elif data[scene][i]['kind'] == 'speech':
        if data[scene][i]['name'] == 'PINK': id = 1
        if data[scene][i]['name'] == 'BLUE': id = 2
        if data[scene][i]['name'] == 'RED': id = 3
        if data[scene][i]['name'] == 'YELLOW': id = 4
        if data[scene][i]['name'] == 'GREEN': id = 5
        if data[scene][i]['size'] == 'small': size = 32
        if data[scene][i]['size'] == 'middle': size = 64
        if data[scene][i]['size'] == 'large': size = 80
        text = data[scene][i]['word']
        action = data[scene][i]['action']
        align = "left"
        voice = re.sub('\n','',text)
        wait = int(len(voice)*0.3)+float(data[scene][i]['wait'])
        print voice
        print wait
        bez.speech(id, voice)                # Voice
        sleep (1)
        bez.dispText(id, text, size, align)  # Text
        bez.act(id, action)                  # Action
        sleep (wait)
        bez.stop()
        cv2.destroyAllWindows()
        i = i+1

      elif data[scene][i]['kind'] == 'select':
        size = 48
        align = 'center'
        bez.dispText(0, data[scene][i]['title'], size, align)  # Text
        size = 32
        bez.dispText(PINK, data[scene][i]['word1'], size, align)  # Text
        bez.dispText(BLUE, data[scene][i]['word2'], size, align)  # Text
        bez.dispText(RED, data[scene][i]['word3'], size, align)  # Text
        bez.dispText(YELLOW, data[scene][i]['word4'], size, align)  # Text
        bez.dispText(GREEN, data[scene][i]['word5'], size, align)  # Text

        while True:                        # 繰り返し処理
          if GPIO.input(17)==GPIO.HIGH:    # 
            scene = data[scene][i]['target1']
            print "PINKスイッチが押されています"
            break
          elif GPIO.input(27)==GPIO.HIGH:    # 
            scene = data[scene][i]['target2']
            print "BLUEスイッチが押されています"
            break
          elif GPIO.input(22)==GPIO.HIGH:    # 
            scene = data[scene][i]['target3']
            print "REDスイッチが押されています"
            break
          elif GPIO.input(23)==GPIO.HIGH:    # 
            scene = data[scene][i]['target4']
            print "YELLOWスイッチが押されています"
            break
          elif GPIO.input(24)==GPIO.HIGH:    # 
            scene = data[scene][i]['target5']
            print "GREENスイッチが押されています"
            break
          else:                            # 
            pass
            # print "スイッチは押されてません"
          sleep (0.1)                      # 0.5秒待つ
        cv2.destroyAllWindows()
        subprocess.call("aplay decided.wav", shell=True)
        i = 0
        sleep (1)
      else:
        print "Not Matched"
  except KeyboardInterrupt:
    print ' 終了しました'

if __name__ == "__main__":
    main()
