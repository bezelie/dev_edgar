#!/usr/bin/python
# -*- coding: utf-8 -*-
# 顔認識デモ
# for Bezelie Flitz
# for Raspberry Pi
# by Jun Toyoda (Team Bezelie)
# from 2018sep15

from datetime import datetime      # 現在時刻取得
from random import randint         # 乱数の発生
from time import sleep             # ウェイト処理
import subprocess                  # 外部プロセスを実行するモジュール
import json                        # jsonファイルを扱うモジュール
import csv                         # CSVファイルを扱うモジュール
import sys                         # python終了sys.exit()のために必要
import picamera                    # カメラ用モジュール
import picamera.array              # カメラ用モジュール
import cv2                         # Open CVモジュール    
import math                        # 絶対値の計算に必要
import bezelie                     # べゼリー専用サーボ制御モジュール

csvFile   = "chatDialog.csv"              # セリフリスト
jsonFile  = "/home/pi/bezelie/dev_edgar/data_face.json"    # 設定ファイル
ttsFile   = "/home/pi/bezelie/dev_edgar/exec_openJTalk.sh" # 音声合成実行ファイル
debugFile = "/home/pi/bezelie/debug.txt"                   # debug用ファイル

# 設定ファイルの読み込み
f = open (jsonFile,'r')
jDict = json.load(f)
name = jDict['data0'][0]['name']       # べゼリーの別名。
user = jDict['data0'][0]['user']       # ユーザーのニックネーム。
vol = jDict['data0'][0]['vol']         # スピーカー音量。
# mic = jDict['data0'][0]['mic']       # マイク感度。62が最大値。

# 変数の初期化
# alarmStop = False   # アラームのスヌーズ機能（非搭載）
# waitTime = 5        # autoモードでの会話の間隔

# OpenCV
cascade_path =  "/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml" # 顔認識xml
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

  # 設定ファイルの読み込み
  f = open (jsonFile,'r')
  jDict = json.load(f)
  vol = jDict['data0'][0]['vol']         # スピーカー音量。
  # mic = jDict['data0'][0]['mic']         # マイク感度の設定。

#  bez.moveRnd()
  subprocess.call('amixer cset numid=1 '+vol+'% -q', shell=True) # スピーカー音量
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
subprocess.call('amixer cset numid=1 '+vol+'% -q', shell=True)      # スピーカー音量
subprocess.call("sh "+ttsFile+" "+u"顔認識するよ", shell=True)

# メインループ
def main():
  try:
    detected = "false"       # 前回顔が認識されたかどうか
    count = 0                # 
    prev_x = 160             # 前回の顔のX座標
    prev_y = 120             # 前回の顔のY座標
    prev_input_x = 0         # 
    prev_input_y = 0         # 
    with picamera.PiCamera() as camera:                         # Open Pi-Camera as camera
      with picamera.array.PiRGBArray(camera) as stream:         # Open Video Stream from Pi-Camera as stream
        camera.resolution = (480, 360)                          # Display Resolution
        camera.hflip = True                                     # Vertical Flip 
        camera.vflip = True                                     # Horizontal Flip
        while True:                                               # infinity loop
          if timeCheck():                                         # 活動時間だったら動く
            camera.capture(stream, 'bgr', use_video_port=True)    # Capture the Video Stream
            gray = cv2.cvtColor(stream.array, cv2.COLOR_BGR2GRAY) # Convert BGR to Grayscale
            facerect = cascade.detectMultiScale(gray,             # Find face from gray
              scaleFactor=1.9,                                    # 1.1 - 1.9 :the bigger the quicker & less acurate 
              minNeighbors=3,                                     # 3 - 6 : the smaller the more easy to detect
              minSize=(120,120),                                    # Minimam face size 
              maxSize=(320,360))                                  # Maximam face size
            if len(facerect) > 0:                                 # If some faces were detected...
              debug_message('detected')
              for rect in facerect:
                cv2.rectangle(stream.array,                       # Draw a rectangle at face place 
                  tuple(rect[0:2]),                               # Upper Left
                  tuple(rect[0:2]+rect[2:4]),                     # Lower Right
                  (0,0,255), thickness=1)                         # Color and thickness
              if detected == "false":
                replyMessage(u"顔認識")
                detected = "true"
                bez.moveAct('swing')
                debug_message('the first detection')
                sleep (0.1)
                bez.stop()
              else:
                debug_message('detected again')
                count = 0
                mindist = 320+240    # 最小距離 (minimum distance)の初期値を理論上の最大値にしておく。
                minindx = 0          # 距離がもっとも近い顔の番号
                indx = 0             # 複数見つかった顔に割り振られる番号
                for rect in facerect: # 前回見つけた顔に一番近い顔を選ぶ
                  dist = math.fabs(rect[0]+rect[2]/2-prev_x) + math.fabs(rect[1]+rect[3]/2-prev_y) # 前回の顔との距離を計算
                  # math.fabsは絶対値。ここで言う距離は正確な距離ではなくX方向の距離とY方向の距離の和。
                  # rect[0]は今回の顔の左上のX座標。rect[2]は今回の顔の四角の横の長さ。
                  if dist < mindist:                             # 今まで最小だった距離よりも小さいなら、これを最小にする。
                    mindist = dist
                    minindx = indx                               # 今回の顔番号を最小の顔の番号とする。
                  indx += 1
                face_x = facerect[minindx][0]+facerect[minindx][2]/2 # 今回ターゲットした顔の中心のX座標
                face_y = facerect[minindx][1]+facerect[minindx][3]/2 # 同じくY座標
                dx = face_x-160     # 画面中央からの横方向のずれ。プラスだったら右より。
                dy = face_y-120     # 同じく縦方向のずれ。
                ratio_x =  0.2        # サーボX方向の回転量
                ratio_y = -0.2        # 同じくY方向
                prev_input_x = int(ratio_x*dx + prev_input_x)
                prev_input_y = int(ratio_y*dy + prev_input_y)
                if prev_input_x > 30:
                  prev_input_x = 30
                if prev_input_x < -30:
                  prev_input_x = -30
                if prev_input_y > 30:
                  prev_input_y = 30
                if prev_input_y < -10:
                  prev_input_y = -10
                bez.moveStage(prev_input_x)
                bez.moveHead(prev_input_y)
                prev_x = face_x     # 今回ターゲットした顔の中心の座標を、次回のために前回の座標とする。
                prev_y = face_y
                sleep (0.5)
                bez.stop()
            else:                   # If no faces were detected.
              debug_message('could not detected')
              bez.moveBack(0)
              count += 1
              if count > 10:
                detected = "false"
                count = 0
                prev_input_y = -1*randint(0,5)          # 乱数を発生させる
                bez.moveHead(prev_input_y)
                angle = randint(1,10)                  # 乱数を発生させる
                if prev_input_x > 0:
                  sign = -1
                else:
                  sign = 1
                prev_input_x = sign*angle
                bez.moveStage(prev_input_x)
                sleep (0.5)
            cv2.imshow('frame', stream.array)                   # 画面に表示したい場合はコメント外してください
            stream.seek(0)                                        # Reset the stream
            stream.truncate()
            if cv2.waitKey(1) & 0xFF == ord('q'):                 # Quit operation
              break
          else:                                                   # 活動時間外は動作しない
            subprocess.call('amixer cset numid=1 60% -q', shell=True)      # スピーカー音量を調整
            subprocess.call("sh "+ttsFile+" "+"活動時間外です", shell=True)
            print "活動時間外なので発声・動作しません"
            sleep (600)   # 10分待機
            subprocess.call('amixer cset numid=1 '+vol+'% -q', shell=True) # スピーカー音量を戻す
        cv2.destroyAllWindows()

  except KeyboardInterrupt: # CTRL+Cで終了
    debug_message('終了します')
    bez.moveCenter()
    sleep (0.2)
    bez.stop()
    sleep (0.1)
    sys.exit(0)

if __name__ == "__main__":
  debug_message('---------- started ----------')
  main()
  sys.exit(0)
