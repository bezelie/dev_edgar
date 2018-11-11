#!/usr/bin/python
# -*- coding: utf-8 -*-
#
 
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy
import sys
import cv2
import flitz
from time import sleep
import subprocess                     # 外部プロセスを実行するモジュール
import RPi.GPIO as GPIO                # GPIO(汎用入出力端子)ライブラリの読み込$

# 変数
ttsRed = "/home/pi/bezelie/dev_edgar/exec_talkRed.sh" # 発話シェルスクリプトのファイル名
ttsBlue = "/home/pi/bezelie/dev_edgar/exec_talkBlue.sh" # 発話シェルスクリプトのファイル名
ttsGreen = "/home/pi/bezelie/dev_edgar/exec_talkGreen.sh" # 発話シェルスクリプトのファイル名
ttsPink = "/home/pi/bezelie/dev_edgar/exec_talkPink.sh" # 発話シェルスクリプトのファイル名
ttsYellow = "/home/pi/bezelie/dev_edgar/exec_talkYellow.sh" # 発話シェルスクリプトのファイル名

# Setting
GPIO.setmode(GPIO.BCM)                 # GPIOをGPIO番号で指定できるように設定
GPIO.setup(17, GPIO.IN)                # GPIOのピンを入力モードに設定
GPIO.setup(27, GPIO.IN)                # GPIOのピンを入力モードに設定
GPIO.setup(22, GPIO.IN)                # GPIOのピンを入力モードに設定
GPIO.setup(23, GPIO.IN)                # GPIOのピンを入力モードに設定
GPIO.setup(24, GPIO.IN)                # GPIOのピンを入力モードに設定
bez = flitz.Control()               # べゼリー操作インスタンスの生成
bez.moveCenter()                     # ０番から７番までのサーボをセンタリング
sleep(0.5)

def drawText(img, text):
  draw = ImageDraw.Draw(img)
  font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",30, encoding="UTF-8")
  img_size = numpy.array(img.size)
  txt_size = numpy.array(font.getsize(text))
  pos = (img_size - txt_size) / 2
  draw.multiline_text((5,0), text, (0, 0, 0), font=font, spacing=15, align='left')

def textSystem(text):
  img = Image.new("RGB", (1200, 60),(200,200,200))
  drawText(img, text)
  filename = "mes0.png"
  img.save(filename)
  img0 = cv2.imread("mes0.png")
  cv2.imshow("MESSAGE",img0)
  cv2.moveWindow("MESSAGE", 300, 100)
  cv2.waitKey(100)

def textPink(text):
  img = Image.new("RGB", (600, 200),(256,200,200))
  drawText(img, text)
  filename = "mes1.png"
  img.save(filename)
  img1 = cv2.imread("mes1.png")
  cv2.imshow("PINK",img1)
  cv2.moveWindow("PINK", 20, 600)
  cv2.waitKey(100)

def textBlue(text):
  img = Image.new("RGB", (600, 200),(100,100,256))
  drawText(img, text)
  filename = "mes2.png"
  img.save(filename)
  img2 = cv2.imread("mes2.png")
  cv2.imshow("BLUE",img2)
  cv2.moveWindow("BLUE", 320, 300)
  cv2.waitKey(100)

def textRed(text):
  img = Image.new("RGB", (600, 200),(256,100,100))
  drawText(img, text)
  filename = "mes3.png"
  img.save(filename)
  img3 = cv2.imread("mes3.png")
  cv2.imshow("RED",img3)
  cv2.moveWindow("RED", 640, 600)
  cv2.waitKey(100)

def textYellow(text):
  img = Image.new("RGB", (600, 200),(256,256,200))
  drawText(img, text)
  filename = "mes4.png"
  img.save(filename)
  img4 = cv2.imread("mes4.png")
  cv2.imshow("YELLOW",img4)
  cv2.moveWindow("YELLOW", 940, 300)
  cv2.waitKey(100)

def textGreen(text):
  img = Image.new("RGB", (600, 200),(200,256,200))
  drawText(img, text)
  filename = "mes5.png"
  img.save(filename)
  img5 = cv2.imread("mes5.png")
  cv2.imshow("GREEN",img5)
  cv2.moveWindow("GREEN", 1260, 600)
  cv2.waitKey(100)

# メインループ
def main():
  try:
    print "開始します"

    text = u'START SCINARIOS'
    textPink(text)
    text = u'INTRODUCTION'
    textBlue(text)
    text = u'MESSAGE FOR OGAKI'
    textRed(text)
    text = u'HOW IT WORKS'
    textYellow(text)
    text = u'DANCE SHOW'
    textGreen(text)
    text = u'PLEASE PUSH ANY SWITCH'
    textSystem(text)

    subprocess.call("aplay end.wav", shell=True)
#    sleep (1)
    cv2.destroyAllWindows()

    while True:                        # 繰り返し処理
      if GPIO.input(17)==GPIO.HIGH:    # GPIO24に3.3Vの電圧がかかっていたら・・$
        print "PINKスイッチが押されています"
        break
      elif GPIO.input(27)==GPIO.HIGH:    # GPIO24に3.3Vの電圧がかかっていたら・$
        print "BLUEスイッチが押されています"
        break
      elif GPIO.input(22)==GPIO.HIGH:    # GPIO24に3.3Vの電圧がかかっていたら・$
        print "REDスイッチが押されています"
        break
      elif GPIO.input(23)==GPIO.HIGH:    # GPIO24に3.3Vの電圧がかかっていたら・$
        print "YELLOWスイッチが押されています"
        break
      elif GPIO.input(24)==GPIO.HIGH:    # GPIO24に3.3Vの電圧がかかっていたら・$
        print "GREENスイッチが押されています"
        break
      else:                            # それ以外の場合は・・・
        pass
        # print "スイッチは押されてません"
      sleep (0.1)                      # 0.5秒待つ

    subprocess.call("aplay decided.wav", shell=True)

    text = u'EPISODE 1'
    textPink(text)
    text = u'EPISODE 2'
    textBlue(text)
    text = u'EPISODE 3'
    textRed(text)
    text = u'EPISODE 4'
    textYellow(text)
    text = u'EPISODE 5'
    textGreen(text)
    text = u'PLEASE PUSH ANY SWITCH'
    textSystem(text)

    bez.act("pitchUpDown")
    subprocess.call("sh "+ttsRed+" "+"僕はべゼリーレッド", shell=True)
    bez.stop()

    cv2.destroyAllWindows()
    sleep (3)

  except KeyboardInterrupt:
    print ' 終了しました'

if __name__ == "__main__":
    main()
