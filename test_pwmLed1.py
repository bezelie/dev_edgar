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

bus = smbus.SMBus(1)

# 変数
jsonFile = "/home/pi/bezelie/edgar/data_chat.json"        # 設定ファイル

class Control(object): # クラスの定義

    # 初期化メソッド。インスタンス生成時に自動実行される。
    def __init__(self, address_pca9685=0x40, dutyMax=490, dutyMin=110, dutyCenter=300, steps=2):
        f = open (jsonFile,'r')
        jDict = json.load(f)
        self.headTrim = int(jDict['data2'][0]['head'])    # トリム値の読み込み
        self.backTrim = int(jDict['data2'][0]['back'])
        self.stageTrim = int(jDict['data2'][0]['stage'])

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
  while True:
    bez.onLed(3)
    sleep (1)
    bez.offLed(3)
    sleep (1)
