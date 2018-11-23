#!/usr/bin/python
# -*- coding: utf-8 -*-
# Bezelie Python Module for Raspberry Pi
# べゼリー専用モジュール

from random import randint         # 乱数の発生
from time import sleep             # ウェイト処理
import RPi.GPIO as GPIO            # GPIO
import smbus                       # I2C
import math                        # 計算用
import threading                   # マルチスレッド処理
import json                        # jsonファイルを扱うモジュール
import subprocess                     # 外部プロセスを実行するモジュール
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy
import sys
import cv2

# CONST
PINK = 1
BLUE = 2
RED = 3
YELLOW = 4
GREEN = 5
bus = smbus.SMBus(1)

# 変数
jsonFile = "/home/pi/bezelie/dev_edgar/trim.json"        # 設定ファイル
ttsRed = "/home/pi/bezelie/dev_edgar/exec_talkRed.sh" # 発話シェルスクリプトのファイル名
ttsBlue = "/home/pi/bezelie/dev_edgar/exec_talkBlue.sh" # 発話シェルスクリプトのファイル名
ttsGreen = "/home/pi/bezelie/dev_edgar/exec_talkGreen.sh" # 発話シェルスクリプトのファイル名
ttsPink = "/home/pi/bezelie/dev_edgar/exec_talkPink.sh" # 発話シェルスクリプトのファイル名
ttsYellow = "/home/pi/bezelie/dev_edgar/exec_talkYellow.sh" # 発話シェルスクリプトのファイル名

class Control(object): # クラスの定義
  def moveCenter(self): # 3つのサーボの回転位置をトリム値に合わせる
    #PINK
    self.moveHead(1, 0)
    self.moveBack(1, 0)
    self.moveStage(1, 0)
    #BLUE
    self.moveHead(2, 0)
    self.moveBack(2, 0)
    self.moveStage(2, 0)
    #RED
    self.moveHead(3, 0)
    self.moveBack(3, 0)
    self.moveStage(3,0)
    #YELLOW
    self.moveHead(4, 0)
    self.moveBack(4, 0)
    self.moveStage(4, 0)
    #GREEN
    self.moveHead(5, 0)
    self.moveBack(5, 0)
    self.moveStage(5, 0)
    sleep (0.5)

# Message ----------------------------

  def drawText(self, img, text, size, align):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", size, encoding="UTF-8")
    if align == 'center':
      img_size = numpy.array(img.size)
      txt_size = numpy.array(font.getsize(text))
      pos = (img_size - txt_size) / 2
      draw.multiline_text(pos, text, (0, 0, 0), font=font, spacing=1, align='center')
    else:
      draw.multiline_text((10,10), text, (0, 0, 0), font=font, spacing=1, align='left')

  def dispText(self, id, text, size, align):
    if id ==0:
      img = Image.new("RGB", (1200, 100),(255,255,255))
      self.drawText(img, text, size, align)
      filename = "mes0.png"
      img.save(filename)
      img0 = cv2.imread("mes0.png")
      cv2.imshow("MESSAGE",img0)
      cv2.moveWindow("MESSAGE", 280, 100)
      cv2.waitKey(150)

    if id ==1:
      img = Image.new("RGB", (600, 200),(256,200,200))
      self.drawText(img, text, size, align)
      filename = "mes1.png"
      img.save(filename)
      img1 = cv2.imread("mes1.png")
      cv2.imshow("PINK",img1)
      cv2.moveWindow("PINK", 20, 600)
      cv2.waitKey(150)

    elif id ==2:
      img = Image.new("RGB", (600, 200),(100,100,256))
      self.drawText(img, text, size, align)
      filename = "mes2.png"
      img.save(filename)
      img2 = cv2.imread("mes2.png")
      cv2.imshow("BLUE",img2)
      cv2.moveWindow("BLUE", 320, 300)
      cv2.waitKey(150)

    elif id ==3:
      img = Image.new("RGB", (600, 200),(256,100,100))
      self.drawText(img, text, size, align)
      filename = "mes3.png"
      img.save(filename)
      img3 = cv2.imread("mes3.png")
      cv2.imshow("RED",img3)
      cv2.moveWindow("RED", 640, 600)
      cv2.waitKey(150)

    elif id ==4:
      img = Image.new("RGB", (600, 200),(256,256,200))
      self.drawText(img, text, size, align)
      filename = "mes4.png"
      img.save(filename)
      img4 = cv2.imread("mes4.png")
      cv2.imshow("YELLOW",img4)
      cv2.moveWindow("YELLOW", 940, 300)
      cv2.waitKey(150)

    elif id ==5:
      img = Image.new("RGB", (600, 200),(200,256,200))
      self.drawText(img, text, size, align)
      filename = "mes5.png"
      img.save(filename)
      img5 = cv2.imread("mes5.png")
      cv2.imshow("GREEN",img5)
      cv2.moveWindow("GREEN", 1260, 600)
      cv2.waitKey(150)

# Action -----------------------------
  def pitchUpLong(self, id, time=2): # 
        while not self.stop_event.is_set():
            self.moveHead(id, 5)
            sleep (time)
            self.moveHead(id, 0)

  def pitchDownLong(self, id, time=2): # 
        while not self.stop_event.is_set():
            self.moveHead(id, -15)
            sleep (time)
            self.moveHead(id, 0)

  def pitchUp2(self, id, time=0.1): # 
        while not self.stop_event.is_set():
            self.moveHead(id, 5)
            self.moveHead(id, 0)
            sleep (time)
            self.moveHead(id, 5)
            self.moveHead(id, 0)
            sleep (time)

  def pitchUpDown(self, id, time=0.5): # 
        while not self.stop_event.is_set():
            self.moveHead(id, 5)
            self.moveHead(id, -10)
            self.moveHead(id, 0)
            sleep (time)

  def pitchUpMax(self, id, time=0.5): # 
        while not self.stop_event.is_set():
            self.moveHead(id, 5)
            sleep (time)
            self.moveHead(id, 0)

  def pitchDownMax(self, id, time=0.5): # 
        while not self.stop_event.is_set():
            self.moveHead(id, -15)
            sleep (time)
            self.moveHead(id, 0)

  def pitchCenter(self, id, time=0.2): # 
        while not self.stop_event.is_set():
            self.moveHead(id, 0)

  def rollRightLeft(self, id, time=0.5): # 
        while not self.stop_event.is_set():
            self.moveBack(id, 20)
            self.moveBack(id, -20)
            self.moveBack(id, 0)
            sleep (time)

  def rollRightLong(self, id, time=2): # 
        while not self.stop_event.is_set():
            self.moveBack(id, 30)
            sleep (time)
            self.moveBack(id, 0)

  def rollRightMax(self, id, time=0.5): # 
        while not self.stop_event.is_set():
            self.moveBack(id, 30)
            sleep (time)
            self.moveBack(id, 0)

  def rollLeftMax(self, id, time=0.5): # 
        while not self.stop_event.is_set():
            self.moveBack(id, -30)
            sleep (time)
            self.moveBack(id, 0)

  def rollCenter(self, id, time=0.2): # 
        while not self.stop_event.is_set():
            self.moveStage(id, 0)

  def yawRightLeft(self, id, time=0.5): # 
        while not self.stop_event.is_set():
            self.moveStage(id, 20)
            self.moveStage(id, -20)
            self.moveStage(id, 0)

  def yawRightMax(self, id, time=2): # 
        while not self.stop_event.is_set():
            self.moveStage(id, 40)
            sleep (time)
            self.moveStage(id, 0)

  def yawLeftMax(self, id, time=2): # 
        while not self.stop_event.is_set():
            self.moveStage(id, -40)
            sleep (time)
            self.moveStage(id, 0)

  def yawCenter(self, id, time=0.2): # 
        while not self.stop_event.is_set():
            self.moveStage(id, 0)

# Initialize -----------------------------
    # 初期化メソッド。インスタンス生成時に自動実行される。
  def __init__(self, address_pca9685=0x40, dutyMax=490, dutyMin=110, dutyCenter=300, steps=2):
        f = open (jsonFile,'r')
        self.jDict = json.load(f)

        # インスタンス変数に値を代入。selfは自分自身のインスタンス名。
        self.address_pca9685 = address_pca9685
        self.dutyMax = dutyMax
        self.dutyMin = dutyMin
        self.dutyCenter = dutyCenter
        self.steps = steps
        self.headNow = dutyCenter
        self.backNow = dutyCenter
        self.stageNow = dutyCenter
        self.initPCA9685()
        # 第１引数はselfにするのが義務。

  def moveHead(self, id, degree, speed=1):
        max = 320     # 下方向の限界
        min = 230     # 上方向の限界
        self.headNow = self.moveServo((id-1)*3+2, degree, int(self.jDict['data'+str(id)][0]['head']), max, min, speed, self.headNow)

  def moveBack(self, id, degree, speed=1):
        max = 380     # 反時計回りの限界
        min = 220     # 時計回りの限界
        self.backNow = self.moveServo((id-1)*3+1, degree, int(self.jDict['data'+str(id)][0]['back']), max, min, speed, self.backNow)

  def moveStage(self, id, degree, speed=1):
        max = 390     # 反時計回りの限界
        min = 210     # 時計回りの限界
        self.stageNow = self.moveServo((id-1)*3, degree, int(self.jDict['data'+str(id)][0]['stage']), max, min, speed, self.stageNow)
        
  def initPCA9685(self):
      try:
        bus.write_byte_data(self.address_pca9685, 0x00, 0x00)
        freq = 0.9 * 50
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq)
        prescaleval -= 1.0
        prescale = int(math.floor(prescaleval + 0.5))
        oldmode = bus.read_byte_data(self.address_pca9685, 0x00)
        newmode = (oldmode & 0x7F) | 0x10
        bus.write_byte_data(self.address_pca9685, 0x00, newmode)
        bus.write_byte_data(self.address_pca9685, 0xFE, prescale)
        bus.write_byte_data(self.address_pca9685, 0x00, oldmode)
        sleep(0.005)
        bus.write_byte_data(self.address_pca9685, 0x00, oldmode | 0xa1)
      except:
        print "サーボドライバーボードを接続してください"
        # pass

  def resetPCA9685(self):
        bus.write_byte_data(self.address_pca9685, 0x00, 0x00)

  def setPCA9685Duty(self, channel, on, off):
        channelpos = 0x6 + 4*channel
        try:
            bus.write_i2c_block_data(self.address_pca9685, channelpos, [on&0xFF, on>>8, off&0xFF, off>>8])
        except IOError:
            pass

  def moveServo(self, id, degree, trim, max, min, speed, now):
        dst = (self.dutyMin - self.dutyMax) * (degree + trim + 90) / 180 + self.dutyMax
        if speed == 0:
            self.setPCA9685Duty_(id, 0, dst)
            sleep(0.001 * math.fabs(dst - now))
            now = dst
        if dst > max:
            dst = max
        if dst < min:
            dst = min
        while (now != dst):
            if now < dst:
                now += self.steps
                if now > dst:
                    now = dst
            else:
                now -= self.steps
                if now < dst:
                    now = dst
            self.setPCA9685Duty(id, 0, now)
            sleep(0.004 * self.steps *(speed))
        return (now)

  def moveRnd(self):
        self.stop_event = threading.Event()
        r = randint(1,7)
        if r == 1:
            self.thread = threading.Thread(target = self.actHappy)
        elif r == 2:
            self.thread = threading.Thread(target = self.actNod)
        elif r == 3:
            self.thread = threading.Thread(target = self.actWhy)
        elif r == 4:
            self.thread = threading.Thread(target = self.actAround)
        elif r == 5:
            self.thread = threading.Thread(target = self.actUp)
        elif r == 6:
            self.thread = threading.Thread(target = self.actWave)
        else:
            self.thread = threading.Thread(target = self.actEtc)
        self.thread.start()

  def act(self, id, act):
    self.stop_event = threading.Event()
    if act == 'pitchUpLong':
        self.thread = threading.Thread(target = self.pitchUpLong, kwargs={'id':id})
    elif act == 'pitchDownLong':
        self.thread = threading.Thread(target = self.pitchDownLong, kwargs={'id':id})
    elif act == 'pitchUp2':
        self.thread = threading.Thread(target = self.pitchUp2, kwargs={'id':id})
    elif act == 'pitchUpDown':
        self.thread = threading.Thread(target = self.pitchUpDown, kwargs={'id':id})
    elif act == 'pitchUpMax':
        self.thread = threading.Thread(target = self.pitchUpMax, kwargs={'id':id})
    elif act == 'pitchDownMax':
        self.thread = threading.Thread(target = self.pitchDownMax, kwargs={'id':id})
    elif act == 'pitchCenter':
        self.thread = threading.Thread(target = self.pitchCenter, kwargs={'id':id})
    elif act == 'rollRightLeft':
        self.thread = threading.Thread(target = self.rollRightLeft, kwargs={'id':id})
    elif act == 'rollRightLong':
        self.thread = threading.Thread(target = self.rollRightLong, kwargs={'id':id})
    elif act == 'rollRightMax':
        self.thread = threading.Thread(target = self.rollRightMax, kwargs={'id':id})
    elif act == 'rollLeftMax':
        self.thread = threading.Thread(target = self.rollLeftMax, kwargs={'id':id})
    elif act == 'rollCenter':
        self.thread = threading.Thread(target = self.rollCenter, kwargs={'id':id})
    elif act == 'yawRightLeft':
        self.thread = threading.Thread(target = self.yawRightLeft, kwargs={'id':id})
    elif act == 'yawRightMax':
        self.thread = threading.Thread(target = self.yawRightMax, kwargs={'id':id})
    elif act == 'yawLeftMax':
        self.thread = threading.Thread(target = self.yawLeftMax, kwargs={'id':id})
    elif act == 'yawCenter':
        self.thread = threading.Thread(target = self.yawCenter, kwargs={'id':id})
    else:
        print "No Action"
    self.thread.start()

# Speech -----------------------------
  def speech(self, id, text):
    self.stop_event = threading.Event()
    if id == 1:
      self.thread = threading.Thread(target = self.speechPink, kwargs={'text':text})
    elif id == 2:
      self.thread = threading.Thread(target = self.speechBlue, kwargs={'text':text})
    elif id == 3:
      self.thread = threading.Thread(target = self.speechRed, kwargs={'text':text})
    elif id == 4:
      self.thread = threading.Thread(target = self.speechYellow, kwargs={'text':text})
    elif id == 5:
      self.thread = threading.Thread(target = self.speechGreen, kwargs={'text':text})
    else:
      print "Not Matched"
    self.thread.start()

  def speechPink(self, text):
    subprocess.call("sh "+ttsPink+" "+text, shell=True)

  def speechBlue(self, text):
    subprocess.call("sh "+ttsBlue+" "+text, shell=True)

  def speechRed(self, text):
    subprocess.call("sh "+ttsRed+" "+text, shell=True)

  def speechYellow(self, text):
    subprocess.call("sh "+ttsYellow+" "+text, shell=True)

  def speechGreen(self, text):
    subprocess.call("sh "+ttsGreen+" "+text, shell=True)

# ---------------------------

  def stop(self):
        self.stop_event.set()
        self.thread.join()

  def onLed(self, channel):
        channelpos = 0x6 + 4*channel
        on = 0
        off = 4095
        try:
            bus.write_i2c_block_data(self.address_pca9685, channelpos, [on&0xFF, on>>8, off&0xFF, off>>8])
        except IOError:
            pass

  def offLed(self, channel):
        channelpos = 0x6 + 4*channel
        on = 0
        off = 0
        try:
            bus.write_i2c_block_data(self.address_pca9685, channelpos, [on&0xFF, on>>8, off&0xFF, off>>8])
        except IOError:
            pass

# スクリプトとして実行された場合はセンタリングを行う
if __name__ == "__main__":
  bez = Control()               # べゼリー操作インスタンスの生成
  bez.moveCenter()
  sleep(1)
