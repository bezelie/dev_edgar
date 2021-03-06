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
import RPi.GPIO as GPIO
import subprocess                  #
import threading                   # マルチスレッド処理
import traceback                   # デバッグ用
import bezelie                     # べゼリー専用モジュール
import socket                      # ソケット通信モジュール
import select                      # 待機モジュール
import json                        #
import csv                         #
import sys
import re

import picamera
import picamera.array
import cv2

csvFile  = "/home/pi/bezelie/edgar/chatDialog.csv"        # 対話リスト
jsonFile = "/home/pi/bezelie/edgar/data_chat.json"        # 設定ファイル
ttsFile  = "/home/pi/bezelie/edgar/exec_openJTalk.sh"     # 音声合成

# 設定ファイルの読み込み
f = open (jsonFile,'r')
jDict = json.load(f)
name = jDict['data0'][0]['name']       # べゼリーの別名。
user = jDict['data0'][0]['user']       # ユーザーのニックネーム。
mic = jDict['data0'][0]['mic']         # マイク感度。62が最大値。
vol = jDict['data0'][0]['vol']         # スピーカー音量。

# 変数の初期化
muteTime = 1        # 音声入力を無視する時間
bufferSize = 256    # 受信するデータの最大バイト。２の倍数が望ましい。
alarmStop = False   # アラームのスヌーズ機能（非搭載）
is_playing = False  # 再生中か否かのフラグ
waitTime = 5        # autoモードでの会話の間隔
mode = True         # Trueなら音声認識モード Falseなら顔認識モード
modePin = 24        # 

# openCV
cascade_path =  "/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml"
cascade = cv2.CascadeClassifier(cascade_path)

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

def alarm():
  global alarmStop
  f = open (jsonFile,'r')
  jDict = json.load(f)
  alarmOn = jDict['data1'][0]['alarmOn']
  alarmTime = jDict['data1'][0]['alarmTime']
  alarmKind = jDict['data1'][0]['alarmKind']
  # alarmVol = jDict['data1'][0]['alarmVol']
  now = datetime.now()
  # print 'Time: '+str(now.hour)+':'+str(now.minute)

  #if True: # アラーム動作のチェック用
  if int(now.hour) == int(alarmTime[0:2]) and int(now.minute) == int(alarmTime[3:5]):
    if alarmOn == "true":
      if alarmStop == False:
        # print 'アラームの時間です'
        subprocess.call('sudo amixer -q sset Mic 0 -c 0', shell=True)  #
        if alarmKind == 'mild':
          bez.moveAct('happy')
          subprocess.call("sh "+ttsFile+" "+"朝ですよ", shell=True)
          bez.stop()
        else:
          bez.moveAct('happy')
          subprocess.call("sh "+ttsFile+" "+"朝だよ起きて起きてー", shell=True)
          bez.stop()
        sleep (muteTime)
        subprocess.call('sudo amixer -q sset Mic '+mic+' -c 0', shell=True)  #
      else:
        # print '_'
        alarmStop = False
    # else:
      # print 'アラームの時間ですが、アラームはオフになっています'

  t=threading.Timer(20,alarm) # ｎ秒後にまたスレッドを起動する
  t.setDaemon(True)           # メインスレッドが終了したら終了させる
  t.start()

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

  maxNum = 0                      # 複数の候補からランダムで選出。data1から欄数値が最大なものを選ぶ
  for i in data1:                 # 
    if i[2] > maxNum:             # 
      maxNum = i[2]               # 
      ansNum = i[3]               #

  debug_message('50: Answer Selected')

  # 発話
  subprocess.call('sudo amixer -q sset Mic 0 -c 0', shell=True)  # 自分の声を認識してしまわないようにマイクを切る
  is_playing = True

  # 設定ファイルの読み込み
  f = open (jsonFile,'r')
  jDict = json.load(f)
  mic = jDict['data0'][0]['mic']         # マイク感度の設定。62が最大値。
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
  #  print "活動時間外なので発声・動作しません"

  alarmStop = True # 対話が発生したらアラームを止める
  subprocess.call('sudo amixer -q sset Mic '+mic+' -c 0', shell=True)  # マイク感受性を元に戻す
  is_playing = False
  debug_message('60: Reply Finished')

def socket_buffer_clear():
  while True:
    rlist, _, _ = select.select([client], [], [], 1)

    if len(rlist) > 0: 
      dummy_buffer = client.recv(bufferSize)
    else:
      break

def parse_recogout(data):
  data = re.search(r'WORD\S+', data)    # \s
  debug_message('30: Got WORD')
  keyWord = data.group().replace("WORD=","").replace("\"","")
  debug_message('40: keyword Parsed= ' + keyWord)
  replyMessage(keyWord)
  debug_message('70')
  socket_buffer_clear()
  debug_message('80')

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

def modeCheck():                   # 音声認識モードか顔認識モードかの判定
  if GPIO.input(24)==GPIO.HIGH:    # GPIO24がHIGHだったら顔認識モードにする
    mode = False
  else:
    mode = True
  return mode

# サーボの初期化
bez = bezelie.Control()                 # べゼリー操作インスタンスの生成
bez.moveCenter()                        # サーボの回転位置をトリム値に合わせる

# GPIOの設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(modePin, GPIO.IN)            # モード(normal/auto)を切り替えたいときに使います。

# TCPクライアントを作成しJuliusサーバーに接続する
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mode = modeCheck()                 # 音声認識モードか顔認識モードかをチェック
if mode == True or mode == False:                   #
  enabled_julius = False
  for count in range(3):
    try:
      client.connect(('localhost', 10500))
      # client.connect(('10.0.0.1', 10500))  # Juliusサーバーに接続
      enabled_julius = True
      break
    except socket.error, e:
      # print 'failed socket connect. retry'
      pass
  if enabled_julius == False:
    print 'boot failed...'
    sys.exit(1)

# メインループ
def main():
  t=threading.Timer(10,alarm)
  t.setDaemon(True)
  t.start()
  try:
    subprocess.call('amixer cset numid=1 '+vol+'% -q', shell=True)      # スピーカー音量
    bez.moveAct('happy')
    subprocess.call('sudo amixer sset Mic 0 -c 0 -q', shell=True)       # マイク感受性
    subprocess.call("sh "+ttsFile+" "+u"こんにちは"+user, shell=True)
    subprocess.call("sh "+ttsFile+" "+u"ぼくは"+name, shell=True)
    subprocess.call('sudo amixer sset Mic '+mic+' -c 0 -q', shell=True) # マイク感受性
    bez.stop()
    sleep (2)
    data = ""
    if mode == True:           # 音声認識モード
      subprocess.call('sh exec_camera.sh', shell=True)            # カメラの映像をディスプレイに表示
      while True:
        if "</RECOGOUT>\n." in data:  # RECOGOUTツリーの最終行を見つけたら以下の処理を行う
          debug_message('20: Recognized')
          parse_recogout(data)
          debug_message('90: Session End')
          data = ""  # 認識終了したのでデータをリセットする
        else:
          debug_message('10: Listening...')
          data = data + client.recv(bufferSize)  # Juliusサーバーから受信
          # /RECOGOUTに達するまで受信データを追加していく
    else:                      # 顔認識モード
      debug_message('face detection mode')
      stageAngle = 0           # ステージの初期角度
      stageDelta = 1           # ループごとにステージを回転させる角度
      stageSpeed = 4           # ループごとにステージを回転させる速度
      with picamera.PiCamera() as camera:                         # Open Pi-Camera as camera
        with picamera.array.PiRGBArray(camera) as stream:         # Open Video Stream from Pi-Camera as stream
          camera.resolution = (600, 400)                          # Display Resolution
          camera.hflip = True                                     # Vertical Flip 
          camera.vflip = True                                     # Horizontal Flip

          while True:
            if "</RECOGOUT>\n." in data:  # RECOGOUTツリーの最終行を見つけたら以下の処理を行う
              debug_message('20: Recognized')
              parse_recogout(data)
              debug_message('90: Session End')
              data = ""  # 認識終了したのでデータをリセットする
            else:
              debug_message('10: Listening...')
              data = data + client.recv(bufferSize)  # Juliusサーバーから受信

              camera.capture(stream, 'bgr', use_video_port=True)    # Capture the Video Stream
              gray = cv2.cvtColor(stream.array, cv2.COLOR_BGR2GRAY) # Convert BGR to Grayscale
              facerect = cascade.detectMultiScale(gray,             # Find face from gray
                scaleFactor=1.9,                                    # 1.1 - 1.9 :the bigger the quicker & less acurate 
                minNeighbors=1,                                     # 3 - 6 : the smaller the more easy to detect
                minSize=(60,100),                                   # Minimam face size 
                maxSize=(400,400))                                  # Maximam face size

              if len(facerect) > 0:
                for rect in facerect:
                  cv2.rectangle(stream.array,                       # Draw a red rectangle at face place 
                    tuple(rect[0:2]),                               # Upper Left
                    tuple(rect[0:2]+rect[2:4]),                     # Lower Right
                    (0,0,255), thickness=2)                         # Color and thickness
                replyMessage(u"顔認識")

              cv2.imshow('frame', stream.array)                     # Display the stream

              if cv2.waitKey(1) & 0xFF == ord('q'):                 # Quit operation
                break

              stream.seek(0)                                        # Reset the stream
              stream.truncate()
            
              stageAngle = stageAngle + stageDelta            
              if stageAngle > 30 or stageAngle < -30:
                stageDelta = stageDelta*(-1)
              bez.moveStage(stageAngle,stageSpeed)

          cv2.destroyAllWindows()

  except KeyboardInterrupt: # CTRL+Cで終了
    debug_message('keyboard interrupted')
    client.close()
    bez.moveCenter()
    bez.stop()
    GPIO.cleanup()                     # ポートをクリア
    sys.exit(0)

if __name__ == "__main__":
  debug_message('---------- started ----------')
  main()
  sys.exit(0)
