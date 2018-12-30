#!/usr/bin/python
# -*- coding: utf-8 -*-
# 音声対話デモ
# for Bezelie Edgar
# for Raspberry Pi
# by Jun Toyoda (Team Bezelie)
# from Aug15th2017

from datetime import datetime      # 現在時刻取得
from random import randint         # 乱数の発生
from time import sleep             # ウェイト処理
import subprocess                  # 外部プロセスを実行するモジュール
import select                      # I/O処理完了待機モジュール
import json                        # jsonファイルを扱うモジュール
import csv                         # CSVファイルを扱うモジュール
import sys                         # python終了sys.exit()のために必要
import re                          # 正規表現モジュール

csvFile   = "/home/pi/bezelie/chatDialog.csv"          # 対話リスト
jsonFile  = "/home/pi/bezelie/edgar/data_chat.json"    # 設定ファイル
ttsFile   = "/home/pi/bezelie/edgar/exec_openJTalk.sh" # 音声合成
debugFile = "/home/pi/bezelie/debug.txt"               # debug用
dataFile = "/home/pi/bezelie/dev_edgar/counter.txt"               # debug用
dataJson = "/home/pi/bezelie/dev_edgar/counter.json"               # debug用

# 設定ファイルの読み込み
def jsonRead():
  f = open (jsonFile,'r')
  jDict = json.load(f)
  name = jDict['data0'][0]['name']       # べゼリーの別名。

def csvRead(keyWord):        # 対話
  data = []                       # 対話ファイル（csv）を変数dataに読み込む
  with open(csvFile, 'rb') as f:  # csvFileをオープン
    for i in csv.reader(f):       # ファイルから１行ずつiに読み込む
      data.append(i)              # dataに追加

def addFile(text):                # デバッグファイル出力機能
  f = open (debugFile,'r')
  textBefore = ""
  for row in f:
    textBefore = textBefore + row
  f.close()
  f = open (debugFile,'w')
  f.write(textBefore + text + "\n")
  f.close()

def readFile():                # デバッグファイル出力機能
  f = open (dataFile,'r')
  textBefore = ""
  for row in f:
    textBefore = textBefore + row
  f.close()
  return textBefore

def writeFile(text):                # デバッグファイル出力機能
  f = open (dataFile,'w')
  f.write(text + "\n")
  f.close()

def debug_message(message):
  t = datetime.now()
  message = str(t.minute)+":"+str(t.second)+":"+message
  print message
#  writeFile(message)
#  sys.stdout.write(message)
#　pass

def getDate():
  t = datetime.now()
  print str(t.year)+str(t.month)+str(t.day)+"-"

# メインループ
def main():
  try:
    count = 0
    while True:
      t = readFile()
      print t
      i = int(t)+1
      writeFile(str(i))
      sleep(1)
  except KeyboardInterrupt: # CTRL+Cで終了
    debug_message(' 終了しました')
    sys.exit(0)

if __name__ == "__main__":
  main()
  sys.exit(0)
