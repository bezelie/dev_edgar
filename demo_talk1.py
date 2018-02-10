#!/usr/bin/python
# -*- coding: utf-8 -*-
# 勝手におしゃべりデモ
# for Bezelie Edgar
# for Raspberry Pi
# by Jun Toyoda (Team Bezelie)
# from Feb2nd2018

from datetime import datetime      # 現在時刻取得
from random import randint         # 乱数の発生
from time import sleep             # ウェイト処理
import RPi.GPIO as GPIO
import subprocess                  #
import bezelie                     # べゼリー専用モジュール
import json                        #
import csv                         #
import sys

csvFile  = "/home/pi/bezelie/dev_edgar/chatDialog.csv"        # 対話リスト
jsonFile = "/home/pi/bezelie/dev_edgar/data_chat.json"        # 設定ファイル
ttsFile  = "/home/pi/bezelie/dev_edgar/exec_openJTalk.sh"     # 音声合成

# 変数の初期値
waitTime = 5                       # しゃべる間隔

# サーボの初期化
bez = bezelie.Control()            # べゼリー操作インスタンスの生成
bez.moveCenter()                   # サーボの回転位置をトリム値に合わせる

# GPIOの設定
GPIO.setmode(GPIO.BCM)

# 関数
def timeCheck(): # 活動時間内かどうかのチェック
  f = open (jsonFile,'r')
  jDict = json.load(f)
  awake1Start = jDict['data1'][0]['awake1Start']
  awake1End = jDict['data1'][0]['awake1End']
  awake2Start = jDict['data1'][0]['awake2Start']
  awake2End  = jDict['data1'][0]['awake2End']
  t = datetime.now()
  if   int(t.hour) >  int(awake1Start[0:2]) and int(t.hour) <    int(awake1End[0:2]):
    flag = True
  elif int(t.hour) == int(awake1Start[0:2]) and int(t.minute) >= int(awake1Start[3:5]):
    flag = True
  elif int(t.hour) == int(awake1End[0:2])   and int(t.minute) <= int(awake1End[3:5]):
    flag = True
  elif int(t.hour) >  int(awake2Start[0:2]) and int(t.hour) <    int(awake2End[0:2]):
    flag = True
  elif int(t.hour) == int(awake2Start[0:2]) and int(t.minute) >= int(awake2Start[3:5]):
    flag = True
  elif int(t.hour) == int(awake2End[0:2])   and int(t.minute) <= int(awake2End[3:5]):
    flag = True
  else:
    flag = False # It is not Active Time
  return flag

def replyMessage():               # 
  data = []                       # 対話ファイル（csv）を変数dataに読み込む
  with open(csvFile, 'rb') as f:  # csvFileをオープン
    for i in csv.reader(f):       # ファイルから１行ずつiに読み込む
      data.append(i)              # dataに追加

  data1 = []                      # 
  for index,i in enumerate(data): # index=連番
    j = randint(1,100)            # １から１００までの乱数を発生させる
    data1.append(i+[j]+[index])   # data1=質問内容,返答,乱数,連番のリスト

  maxNum = 0                      # data1から欄数値が最大なものを選ぶ
  for i in data1:                 # 
    if i[2] > maxNum:             # 
      maxNum = i[2]               # 
      ansNum = i[3]               #

  debug_message(data[ansNum][1])

  # 設定ファイルの読み込み
  f = open (jsonFile,'r')
  jDict = json.load(f)
  vol = jDict['data0'][0]['vol']         # 

  if timeCheck(): # 活動時間だったら会話する
    bez.moveRnd()
    subprocess.call('amixer cset numid=1 '+vol+'% -q', shell=True) # スピーカー音量
    subprocess.call("sh "+ttsFile+" "+data[ansNum][1], shell=True)
    bez.stop()
  else:           # 活動時間外は会話しない
    subprocess.call('amixer cset numid=1 60% -q', shell=True)      # スピーカー音量
    subprocess.call("sh "+ttsFile+" "+"活動時間外です", shell=True)
    sleep (5)
    subprocess.call('amixer cset numid=1 '+vol+'% -q', shell=True) # スピーカー音量

def debug_message(message):
  print message
#　pass
#  writeFile(message)
#  sys.stdout.write(message)

def writeFile(text): # デバッグファイル出力機能
  f = open ('debug.txt', 'r')
  textBefore = ""
  for row in f:
    textBefore = textBefore + row
  f.close()
  f = open ('debug.txt', 'w')
  f.write(textBefore + text + "\n")
  f.close()

# Main Loop
def main():
  try:
    data = ""
    bez.moveAct('happy')
    f = open (jsonFile,'r')
    jDict = json.load(f)
    name = jDict['data0'][0]['name']       # べゼリーの別名。
    user = jDict['data0'][0]['user']       # ユーザーのニックネーム。
    vol = jDict['data0'][0]['vol']         # スピーカー音量。
    subprocess.call('amixer cset numid=1 '+vol+'% -q', shell=True)      # スピーカー音量
    subprocess.call("sh "+ttsFile+" "+u"こんにちは"+user, shell=True)
    subprocess.call("sh "+ttsFile+" "+u"ぼくは"+name, shell=True)
    bez.stop()
    while True:
      sleep(waitTime)
      replyMessage()

  except KeyboardInterrupt: # CTRL+Cで終了
    debug_message('keyboard interrupted')
    bez.stop()
    sys.exit(0)

if __name__ == "__main__":
  debug_message('---------- started ----------')
  main()
  sys.exit(0)
