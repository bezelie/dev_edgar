# -*- coding: utf-8 -*-
# 音声対話デモ
# for Bezelie Edgar
# for Raspberry Pi
# by Jun Toyoda (Team Bezelie)
# from Aug15th2017

from datetime import datetime      # 現在時刻取得
from random import randint         # 乱数の発生
from time import sleep             # ウェイト処理
import bezelie                     # べゼリー専用モジュール
import xml.etree.ElementTree as ET # XMLエレメンタルツリー変換モジュール
import subprocess                  #
import threading                   # マルチスレッド処理
import socket                      # ソケット通信モジュール
import json                        #
import csv                         #

csvFile       = "/home/pi/bezelie/dev_edgar/chatDialog.csv"     # 対話リスト
jsonFile      = "/home/pi/bezelie/dev_edgar/data_chat.json"     # 設定ファイル
openJTalkFile = "/home/pi/bezelie/dev_edgar/exec_openJTalk.sh"  # 音声合成
sensitivity = 50                   # マイク感度の設定。62が最大値。

# Variables
muteTime = 0.5    # 音声入力を無視する時間
bufferSize = 512  # 受信するデータの最大バイト数。できるだけ小さな２の倍数が望ましい。
alarmStop = False # アラームのスヌーズ機能（非搭載）

# Servo Setting
bez = bezelie.Control()               # べゼリー操作インスタンスの生成
bez.setTrim(head=0, back=-5, stage=0) # センター位置の微調整
bez.moveCenters()                     # ０番から７番までのサーボをセンタリング
sleep(0.5)

# TCPクライアントを作成しJuliusサーバーに接続する
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(('10.0.0.1', 10500))  # Juliusサーバーに接続
client.connect(('localhost', 10500))  # Juliusサーバーに接続

# Functions
def replyMessage(keyWord):        # 対話
  data = []                       # 対話ファイル（csv）を変数dataに読み込む
  with open(csvFile, 'rb') as f:  #
    for i in csv.reader(f):
      data.append(i)              # raw data

  data1 = []                      # dataから質問内容がキーワードに一致している行をdata1として抜き出す
  for index,i in enumerate(data): #
    if unicode(i[0], 'utf-8')==keyWord:  # i[0]はstrなのでutf-8に変換して比較する必要がある
      j = randint(1,100)          # １から１００までの乱数を発生させる
      data1.append(i+[j]+[index]) # data1=質問内容,返答,乱数,連番のリスト

  if data1 == []:                 # data1が空っぽだったら質問内容は不一致として処理する
    for index,i in enumerate(data): 
      if i[0]=='不一致':           
        j = randint(1,100)         
        data1.append(i+[j]+[index])

  maxNum = 0                      # data1から欄数値が最大なものを選ぶ
  for i in data1:                 # 
    if i[2] > maxNum:             # 
      maxNum = i[2]               # 
      ansNum = i[3]               #

  # 発話
  subprocess.call('sudo amixer -q sset Mic 0 -c 0', shell=True)  # 自分の声を認識してしまわないようにマイクを切る
  print "Bezelie..."+data[ansNum][1]

  if timeCheck(): # 活動時間だったら会話する
    bez.moveRnd()
    subprocess.call("sh "+openJTalkFile+" "+data[ansNum][1], shell=True)
    bez.stop()
  else:           # 活動時間外は会話しない
    subprocess.call('amixer cset numid=1 70% -c 0', shell=True)                          # スピーカー音量
    subprocess.call("sh "+openJTalkFile+" "+"活動時間外です", shell=True)
    sleep (5)
    subprocess.call('amixer cset numid=1 100% -c 0', shell=True)                          # スピーカー音量
  #  print "活動時間外なので発声・動作しません"

  alarmStop = True # 対話が発生したらアラームを止める
  sleep (muteTime)
  subprocess.call('sudo amixer -q sset Mic '+str(sensitivity)+' -c 0', shell=True)  # マイク感受性を元に戻す

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

def alarm():
  global alarmStop
  f = open (jsonFile,'r')
  jDict = json.load(f)
  alarmOn = jDict['data1'][0]['alarmOn']
  alarmTime = jDict['data1'][0]['alarmTime']
  alarmKind = jDict['data1'][0]['alarmKind']
  # alarmVol = jDict['data1'][0]['alarmVol']
  now = datetime.now()
  print 'Time: '+str(now.hour)+':'+str(now.minute)

  #if True: # アラーム動作のチェック用
  if int(now.hour) == int(alarmTime[0:2]) and int(now.minute) == int(alarmTime[3:5]):
    if alarmOn == "true":
      if alarmStop == False:
        print 'アラームの時間です'
        subprocess.call('sudo amixer -q sset Mic 0', shell=True)  #
        if alarmKind == 'mild':
          bez.moveAct('happy')
          subprocess.call("sh "+openJTalkFile+" "+"朝ですよ", shell=True)
          bez.stop()
        else:
          bez.moveAct('happy')
          subprocess.call("sh "+openJTalkFile+" "+"朝だよ起きて起きてー", shell=True)
          bez.stop()
        sleep (muteTime)
        subprocess.call('sudo amixer -q sset Mic '+str(sensitivity), shell=True)  #
      else:
        print '_'
        alarmStop = False
    else:
      print 'アラームの時間ですが、アラームはオフになっています'
  t=threading.Timer(20,alarm) # ｎ秒後にまたスレッドを起動する
  t.setDaemon(True)           # メインスレッドが終了したら終了させる
  t.start()

def writeFile(text): # デバッグファイル（out.txt）出力機能
  f = open ('out.txt', 'r')
  textBefore = ""
  for row in f:
    textBefore = textBefore + row
  f.close()
  f = open ('out.txt', 'w')
  f.write(textBefore + text + "\n")
  f.write(str(type(textBefore)))
  f.write(str(type(text)))
  f.write(str(type(textBefore + text)))
  f.close()
  sleep(0.1)

# Set up
subprocess.call('amixer cset numid=1 100% -c 0', shell=True)                          # スピーカー音量
subprocess.call('sudo amixer -q sset Mic '+str(sensitivity)+' -c 0', shell=True) # マイク感受性

t=threading.Timer(10,alarm)
t.setDaemon(True)
t.start()

# Main Loop
def main():
#  writeFile("main start ----------------------------")
  try:
    data = ""
    print "Please Speak"
    bez.moveAct('happy')
    subprocess.call("sh "+openJTalkFile+" "+"起動完了", shell=True)
    bez.stop()
    while True:
      if "</RECOGOUT>\n." in data:  # RECOGOUTツリーの最終行を見つけたら以下の処理を行う
        try:
          # dataから必要部分だけ抽出し、かつエラーの原因になる文字列を削除する。
          data = data[data.find("<RECOGOUT>"):].replace("\n.", "")
          # fromstringはXML文字列からコンテナオブジェクトであるElement型に直接変換するメソッド
          root = ET.fromstring('<?xml version="1.0" encoding="utf-8" ?>\n' + data)
          keyWord = ""
          for whypo in root.findall("./SHYPO/WHYPO"):
            keyWord = keyWord + whypo.get("WORD")
          replyMessage(keyWord)
        except:
          print "----- except -------------------"
        data = ""  # 認識終了したのでデータをリセットする
      else:
        data = data + client.recv(bufferSize)  # Juliusサーバーから受信
        # /RECOGOUTに達するまで受信データを追加していく

  except KeyboardInterrupt: # CTRL+Cで終了
    print "  終了しました"
    client.close()
    bez.stop()

if __name__ == "__main__":
#    pass
    main()
