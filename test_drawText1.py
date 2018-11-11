#!/usr/bin/python
# -*- coding: utf-8 -*-
#
 
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy
import sys
import cv2
import bezelie
from time import sleep

def drawText(img, text):
  draw = ImageDraw.Draw(img)
  font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",30, encoding="UTF-8")
  img_size = numpy.array(img.size)
  txt_size = numpy.array(font.getsize(text))
  pos = (img_size - txt_size) / 2
  draw.multiline_text((5,0), text, (0, 0, 0), font=font, spacing=15, align='left')

img = Image.new("RGB", (1200, 100),(256,256,256))
text = u'mmm'
drawText(img, text)
img.show()
filename = "mes0.png"
img.save(filename)

img = Image.new("RGB", (600, 200),(256,200,200))
text = u'ライブラリの読み込ライブラリの\n読みライブラリ'
drawText(img, text)
filename = "mes1.png"
img.save(filename)

img = Image.new("RGB", (600, 200),(100,100,256))
text = u'ライブラリの読み'
drawText(img, text)
filename = "mes2.png"
img.save(filename)

img = Image.new("RGB", (600, 200),(256,100,100))
text = u'ライブラリの読'
drawText(img, text)
filename = "mes3.png"
img.save(filename)

img = Image.new("RGB", (600, 200),(256,256,200))
text = u'ライブラリの読み'
drawText(img, text)
filename = "mes4.png"
img.save(filename)

img = Image.new("RGB", (600, 200),(200,256,200))
text = u'ライブラリの読'
drawText(img, text)
filename = "mes5.png"
img.save(filename)

img0 = cv2.imread("mes0.png")
cv2.imshow("MESSAGE",img0)
cv2.moveWindow("MESSAGE", 280, 340)
cv2.waitKey(100)
#cv2.destroyWindow("img0")

img1 = cv2.imread("mes1.png")
cv2.imshow("ライブ",img1)
cv2.moveWindow("ライブ", 20, 500)
cv2.waitKey(100)
#cv2.destroyWindow("img1")

img2 = cv2.imread("mes2.png")
cv2.imshow("イブラ",img2)
cv2.moveWindow("イブラ", 320, 100)
cv2.waitKey(100)
#cv2.destroyWindow("img2")

img3 = cv2.imread("mes3.png")
cv2.imshow("ブラリ",img3)
cv2.moveWindow("ブラリ", 640, 500)
cv2.waitKey(100)
#cv2.destroyWindow("img3")

img4 = cv2.imread("mes4.png")
cv2.imshow("ブラ",img4)
cv2.moveWindow("ブラ", 940, 100)
cv2.waitKey(100)
#cv2.destroyWindow("img4")

img5 = cv2.imread("mes5.png")
cv2.imshow("ラリ",img5)
cv2.moveWindow("ラリ", 1260, 500)
cv2.waitKey(100)
#cv2.destroyWindow("img5")
sleep (3)


