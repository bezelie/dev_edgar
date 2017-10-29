# -*- coding: utf-8 -*-
# Bezelie Python Module for Raspberry Pi
import RPi.GPIO as GPIO
from time import sleep
from random import randint
import smbus # for I2C
import math
import threading

bus = smbus.SMBus(1)

class Control(object): # クラスの定義。ユーザー定義のクラスは大文字から始めるのが習慣。

    # 初期化メソッド。インスタンス生成時に自動実行される。
    def __init__(self, address_pca9685=0x40, dutyMax=490, dutyMin=110, dutyCenter=300, steps=1):
        # インスタンス変数に値を代入。selfは自分自身のインスタンス名。
        self.address_pca9685 = address_pca9685
        self.dutyMax = dutyMax
        self.dutyMin = dutyMin
        self.dutyCenter = dutyCenter
        self.steps = steps
        self.headTrim = 0
        self.backTrim = 0
        self.stageTrim = 0
        self.headNow = dutyCenter
        self.backNow = dutyCenter
        self.stageNow = dutyCenter
        self.initPCA9685()
        # 第１引数はselfにするのが義務。

    def moveHead(self, degree, speed=1):
        max = 320     # Downward limit
        min = 230     # Upward limit
        self.headNow = self.moveServo(2, degree, self.headTrim, max, min, speed, self.headNow)

    def moveBack(self, degree, speed=1):
        max = 380     # AntiClockwise limit
        min = 220     # Clockwise limit
        self.backNow = self.moveServo(1, degree, self.backTrim, max, min, speed, self.backNow)

    def moveStage(self, degree, speed=1):
        max = 390    # AntiClockWise limit
        min = 210    # Clocwise limit
        self.stageNow = self.moveServo(0, degree, self.stageTrim, max, min, speed, self.stageNow)

    def moveCenter(self):
        self.moveHead (0)
        self.moveBack (0)
        self.moveStage (0)

    def moveCenters(self): # ０番から3番までのサーボをセンタリングする
        for i in range (0,3):
            self.moveServo(i, 0, 0, 390, 210, 1, self.dutyCenter+20)
            sleep (0.1)
        for i in range (0,3):
            self.moveServo(i, 0, 0, 390, 210, 1, self.dutyCenter-20)
            sleep (0.1)
        for i in range (0,3):
            self.moveServo(i, 0, 0, 390, 210, 1, self.dutyCenter)
            sleep (0.1)

    def setTrim(self, head=None, back=None, stage=None):
        if head is not None:
            self.headTrim = head;
        if back is not None:
            self.backTrim = back;
        if stage is not None:
            self.stageTrim = stage;

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
        print "Please connect PCA9685 to RaspberryPi"

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

    '''
    def centering(self):
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target = self.centerings)
        self.thread.start()

    def centerings(self):
        for i in range (0,8):
            self.setPCA9685Duty(i, 0, self.dutyCenter-64)
            sleep(0.1)
        for i in range (0,8):
            self.setPCA9685Duty(i, 0, self.dutyCenter+64)
            sleep(0.1)
        for i in range (0,8):
            self.setPCA9685Duty(i, 0, self.dutyCenter)
            sleep(0.1)
    '''

    def moveRnd(self):
        self.stop_event = threading.Event()
        r = randint(1,3)
        if r == 1:
            self.thread = threading.Thread(target = self.actHappy)
        elif r == 2:
            self.thread = threading.Thread(target = self.actNod)
        else:
            self.thread = threading.Thread(target = self.actWhy)
        self.thread.start()

    def moveAct(self, act):
        self.stop_event = threading.Event()
        if act == 'happy':
            self.thread = threading.Thread(target = self.actHappy)
        elif act == 'nod':
            self.thread = threading.Thread(target = self.actNod)
        else:
            self.thread = threading.Thread(target = self.actWhy)
        self.thread.start()

    def actHappy(self, time=0.5):
        while not self.stop_event.is_set():
            self.moveHead(20)
            self.moveBack(10)
            self.moveBack(-10)
            self.moveBack(10)
            self.moveBack(-10)
            self.moveBack(0)
            sleep (time)
            self.moveHead(0)  
  
    def actNod(self, time=0.5):
        while not self.stop_event.is_set():
            self.moveHead(-10)
            self.moveHead(0)  
            self.moveHead(-10)
            sleep (time)
            self.moveHead(0)  

    def actWhy(self, time=1): # 首かしげ
        while not self.stop_event.is_set():
            self.moveBack(15)
            sleep (time)
            self.moveBack(0)

    def stop(self):
        self.stop_event.set()
        self.thread.join()

