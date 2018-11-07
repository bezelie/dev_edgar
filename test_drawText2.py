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

img = Image.new("RGB", (600, 200),(256,100,100))
text = u'ライブラリの読み込ライブラリの\n読みライラリ'
drawText(img, text)
# img.show()
filename = "mes1.png"
img.save(filename)

img1 = cv2.imread("mes1.png")
cv2.imshow("RED",img1)
cv2.moveWindow("RED", 20, 500)
cv2.waitKey(100)
sleep (1)
cv2.destroyWindow("RED")


