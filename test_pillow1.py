#!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy
import sys

def drawText(img, text):
  draw = ImageDraw.Draw(img)
  draw.font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",30)
  img_size = numpy.array(img.size)
  txt_size = numpy.array(draw.font.getsize(text))
  pos = (img_size - txt_size) / 2
  draw.text(pos, text, (0, 0, 255))

img = Image.new("RGBA", (400, 80))
text = u'ライブラリの読み込'
drawText(img, text)
img.show()
filename = "out.png"
img.save(filename)
