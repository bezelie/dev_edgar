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

# 変数
ttsRed = "/home/pi/bezelie/dev_edgar/exec_talkRed.sh" # 発話シェルスクリプトのファイル名
ttsBlue = "/home/pi/bezelie/dev_edgar/exec_talkBlue.sh" # 発話シェルスクリプトのファイル名
ttsGreen = "/home/pi/bezelie/dev_edgar/exec_talkGreen.sh" # 発話シェルスクリプトのファイル名
ttsPink = "/home/pi/bezelie/dev_edgar/exec_talkPink.sh" # 発話シェルスクリプトのファイル名
ttsYellow = "/home/pi/bezelie/dev_edgar/exec_talkYellow.sh" # 発話シェルスクリプトのファイル名

# Setting
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

# メインループ
def main():
  try:
    print "開始します"

    img = Image.new("RGB", (1200, 60),(200,200,200))
    text = u'S T A R T !'
    drawText(img, text)
    filename = "mes0.png"
    img.save(filename)

    img0 = cv2.imread("mes0.png")
    cv2.imshow("MESSAGE",img0)
    cv2.moveWindow("MESSAGE", 280, 340)
    cv2.waitKey(100)
    subprocess.call("aplay decided.wav", shell=True)
#    sleep (1)
    cv2.destroyWindow("MESSAGE")

    while (True):

      img = Image.new("RGB", (600, 200),(256,200,200))
      text = u'ライブラリの読み込ライブラリの\n読みライブラリ'
      drawText(img, text)
      filename = "mes1.png"
      img.save(filename)

      img1 = cv2.imread("mes1.png")
      cv2.imshow("ライブ",img1)
      cv2.moveWindow("ライブ", 20, 500)
      cv2.waitKey(150)
      bez.act("pitchUpDown")
      subprocess.call("sh "+ttsRed+" "+"僕はべゼリーレッド", shell=True)
      cv2.destroyWindow("ライブ")
      bez.stop()
  except KeyboardInterrupt:
    print ' 終了しました'

if __name__ == "__main__":
    main()
