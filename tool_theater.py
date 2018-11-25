#!/usr/bin/python
# -*- coding: utf-8 -*-
# scenario converter
import cv2
from time import sleep
import subprocess                  # 外部プロセスを実行するモジュール
import json                        # jsonファイルを扱うモジュール
import RPi.GPIO as GPIO            # GPIO(汎用入出力端子)ライブラリの読み込$
import re                          # 正規表現モジュール
import math                        # 計算用
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy

# CONST
PINK   = 1
BLUE   = 2
RED    = 3
YELLOW = 4
GREEN  = 5
scenarioNum = 9

# 変数
scenarioFile = "/home/pi/bezelie/dev_edgar/theater.json"        # 設定ファイル
ttsRed = "/home/pi/bezelie/dev_edgar/exec_talkRed.sh" # 発話シェルスクリプトのファイル名
ttsBlue = "/home/pi/bezelie/dev_edgar/exec_talkBlue.sh" # 発話シェルスクリプトのファイル名
ttsGreen = "/home/pi/bezelie/dev_edgar/exec_talkGreen.sh" # 発話シェルスクリプトのファイル名
ttsPink = "/home/pi/bezelie/dev_edgar/exec_talkPink.sh" # 発話シェルスクリプトのファイル名
ttsYellow = "/home/pi/bezelie/dev_edgar/exec_talkYellow.sh" # 発話シェルスクリプトのファイル名

# Setting

# Message ----------------------------

def drawText(img, text, size, align):
  draw = ImageDraw.Draw(img)
  font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", size, encoding="UTF-8")
  if align == 'center':
    img_size = numpy.array(img.size)
    txt_size = numpy.array(font.getsize(text))
    pos = (img_size - txt_size) / 2
    draw.multiline_text(pos, text, (0, 0, 0), font=font, spacing=1, align='center')
  else:
    draw.multiline_text((10,10), text, (0, 0, 0), font=font, spacing=1, align='left')

def dispText(id, text, size, align, sce, i):
  if id ==0:
    img = Image.new("RGB", (1220, 100),(255,255,255))
    drawText(img, text, size, align)
    filename = "scenario/"+str(sce)+"-"+str(i)+".png"
    img.save(filename)

  if id ==1:
    img = Image.new("RGB", (600, 200),(256,200,200))
    drawText(img, text, size, align)
    filename = "scenario/"+str(sce)+"-"+str(i)+".png"
    img.save(filename)

  elif id ==2:
    img = Image.new("RGB", (600, 200),(100,100,256))
    drawText(img, text, size, align)
    filename = "scenario/"+str(sce)+"-"+str(i)+".png"
    img.save(filename)

  elif id ==3:
    img = Image.new("RGB", (600, 200),(256,100,100))
    drawText(img, text, size, align)
    filename = "scenario/"+str(sce)+"-"+str(i)+".png"
    img.save(filename)

  elif id ==4:
    img = Image.new("RGB", (600, 200),(256,256,200))
    drawText(img, text, size, align)
    filename = "scenario/"+str(sce)+"-"+str(i)+".png"
    img.save(filename)

  elif id ==5:
    img = Image.new("RGB", (600, 200),(200,256,200))
    drawText(img, text, size, align)
    filename = "scenario/"+str(sce)+"-"+str(i)+".png"
    img.save(filename)

# Speech -----------------------------
def speech(id, text, sce, i):
  if id == 1:
    subprocess.call("sh "+ttsPink+" "+text, shell=True)
  elif id == 2:
    subprocess.call("sh "+ttsBlue+" "+text, shell=True)
  elif id == 3:
    subprocess.call("sh "+ttsRed+" "+text, shell=True)
  elif id == 4:
    subprocess.call("sh "+ttsYellow+" "+text, shell=True)
  elif id == 5:
    subprocess.call("sh "+ttsGreen+" "+text, shell=True)
  else:
    print "Not Matched"
  subprocess.call("sudo cp /tmp/voice.wav "+"scenario/"+str(sce)+"-"+str(i)+".wav", shell=True)
  

# ---------------------------


# メインループ
def main():
  try:
    print "開始します"
    f = open (scenarioFile,'r')
    data = json.load(f)
    i = 0
    sce = 0
    scene = 'scene0'
    while sce < scenarioNum + 1:
      print "scene="+scene
      print "talk ="+str(i)
      if data[scene][i]['kind'] == 'title':
        text = data[scene][i]['word']
        size = 80
        align = 'center'
        dispText(0, text, size, align, sce, i)  # Text
        i = i+1
      elif data[scene][i]['kind'] == 'end':
        text = u'おしまい'
        size = 80
        align = 'center'
        dispText(0, text, size, align, sce, i)  # Text
        i = 0
        sce = sce + 1
        scene = 'scene'+str(sce)
      elif data[scene][i]['kind'] == 'speech':
        # data input
        size = 32
        if data[scene][i]['name'] == 'PINK': id = 1
        if data[scene][i]['name'] == 'BLUE': id = 2
        if data[scene][i]['name'] == 'RED': id = 3
        if data[scene][i]['name'] == 'YELLOW': id = 4
        if data[scene][i]['name'] == 'GREEN': id = 5
        if data[scene][i]['size'] == 'small': size = 48
        if data[scene][i]['size'] == 'middle': size = 64
        if data[scene][i]['size'] == 'large': size = 80
        text = data[scene][i]['word']
        align = "left"
        voice = re.sub('\n','',text)
        print voice
        # action
        speech(id, voice, sce, i)                # Voice
        dispText(id, text, size, align, sce, i)  # Text
        i = i+1

      elif data[scene][i]['kind'] == 'select':
        size = 64
        align = 'center'
        dispText(0, data[scene][i]['title'], size, align, sce, 0)  # Text
        size = 48
        dispText(PINK, data[scene][i]['word1'], size, align, sce, 1)  # Text
        dispText(BLUE, data[scene][i]['word2'], size, align, sce, 2)  # Text
        dispText(RED, data[scene][i]['word3'], size, align, sce, 3)  # Text
        dispText(YELLOW, data[scene][i]['word4'], size, align, sce, 4)  # Text
        dispText(GREEN, data[scene][i]['word5'], size, align, sce, 5)  # Text
        i = 0
        sce = sce + 1
        scene = 'scene'+str(sce)
      else:
        print "Not Matched"
  except KeyboardInterrupt:
    print ' 終了しました'

if __name__ == "__main__":
    main()
