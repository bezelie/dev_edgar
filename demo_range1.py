#!/usr/bin/python
# -*- coding: utf-8 -*-
# 顔認識デモ
# for Bezelie Flitz
# for Raspberry Pi
# by Jun Toyoda (Team Bezelie)
# from 2018sep15

from random import randint         # 乱数の発生
from time import sleep
import time
import subprocess                  # 外部プロセスを実行するモジュール
import json                        # jsonファイルを扱うモジュール
import csv                         # CSVファイルを扱うモジュール
import sys                         # python終了sys.exit()のために必要
import picamera                    # カメラ用モジュール
import picamera.array              # カメラ用モジュール
import cv2                         # Open CVモジュール    
import math                        # 絶対値の計算に必要
import bezelie                     # べゼリー専用サーボ制御モジュール
import RPi.GPIO as GPIO

# Definition
trigger_pin = 18    # GPIO 18
echo_pin = 23       # GPIO 23
actionDistance = 30 # centi mater
GPIO.setmode(GPIO.BCM)
GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

csvFile   = "rangeDialog.csv"              # セリフリスト
jsonFile  = "/home/pi/bezelie/dev_edgar/data_chat.json"    # 設定ファイル
ttsFile   = "/home/pi/bezelie/dev_edgar/exec_openJTalk.sh" # 音声合成実行ファイル
debugFile = "/home/pi/bezelie/debug.txt"                   # debug用ファイル

# OpenCV
cascade_path =  "/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml" # 顔認識xml
cascade = cv2.CascadeClassifier(cascade_path)

# 関数
def send_trigger_pulse():
    GPIO.output(trigger_pin, True)
    sleep(0.0001)
    GPIO.output(trigger_pin, False)

def wait_for_echo(value, timeout):
    count = timeout
    while GPIO.input(echo_pin) != value and count > 0:
        count -= 1

def get_distance():
    send_trigger_pulse()
    wait_for_echo(True, 10000)
    start = time.time()
    wait_for_echo(False, 10000)
    finish = time.time()
    pulse_len = finish - start
    distance  = pulse_len / 0.000058
    return (distance)    


def replyMessage(keyWord):        # 対話
  data = []                       # 対話ファイル（csv）を変数dataに読み込む
  with open(csvFile, 'rb') as f:  # csvFileをオープン
    for i in csv.reader(f):       # ファイルから１行ずつiに読み込む
      data.append(i)              # dataに追加

  data1 = []                      # dataから質問内容がキーワードに一致している行をdata1として抜き出す
  for index,i in enumerate(data): # index=連番
    if unicode(i[0], 'utf-8')==keyWord:  # i[0]はstrなのでutf-8に変換して比較する必要がある
      j = randint(1,100)          # １から１００までの乱数を発生させる
      data1.append(i+[j]+[index]) # data1=質問内容,返答,乱数,連番のリスト

  if data1 == []:                 # data1が空っぽだったらランダムで返す
    for index,i in enumerate(data): 
      j = randint(1,100)         
      data1.append(i+[j]+[index])

  maxNum = 0                      # data1の候補から乱数値が最大なものを選ぶ
  for i in data1:                 
    if i[2] > maxNum:              
      maxNum = i[2]                
      ansNum = i[3]               

#  bez.moveRnd()
  subprocess.call("sh "+ttsFile+" "+data[ansNum][1], shell=True)
#  bez.stop()

def debug_message(message):
  print message
#  writeFile(message)
#　pass
#  sys.stdout.write(message)

def writeFile(text):                    # デバッグファイル出力機能
  f = open (debugFile,'r')
  textBefore = ""
  for row in f:
    textBefore = textBefore + row
  f.close()
  f = open (debugFile,'w')
  f.write(textBefore + text + "\n")
  f.close()

# サーボの初期化
bez = bezelie.Control()                 # べゼリー操作インスタンスの生成
bez.moveCenter()                        # サーボの回転位置をトリム値に合わせる

# 初回処理
subprocess.call("sh "+ttsFile+" "+u"距離センサーで反応するよ", shell=True)

# メインループ
def main():
  try:
    detected = "false"       # 前回顔が認識されたかどうか
    count = 0                # 
    meet = 0
    while True:                                               # infinity loop
      d = get_distance()
      print(round(d,1))
      if d < actionDistance:                        # If some faces were detected...
        debug_message('detected')
        if detected == "false":
          meet = 1
          replyMessage(u"顔発見")
          detected = "true"
          bez.moveAct('swing')
          debug_message('the first detection')
          sleep (0.1)
          bez.stop()
        else:
          meet = meet +1
          if meet > 3:
            replyMessage(u"顔認識")
            meet = 1
          debug_message('detected again')
          count = 0
          bez.moveRnd()
          sleep (1)
          bez.stop()
      else:                   # If no faces were detected.
        debug_message('could not detected')
        meet = 0
        count += 1
        if count > 10:
          replyMessage(u"未発見")
          detected = "false"
          count = 0
        sleep (1)

  except KeyboardInterrupt: # CTRL+Cで終了
    debug_message('終了します')
    bez.moveCenter()
    sleep (0.2)
    bez.stop()
    sleep (0.1)
    GPIO.cleanup
    sys.exit(0)

if __name__ == "__main__":
  debug_message('---------- started ----------')
  main()
  GPIO.cleanup
  sys.exit(0)
