# -*- coding: utf-8 -*-
# Bezelie demo Code for Raspberry Pi : Camera and Range Sensor

import RPi.GPIO as GPIO
from time import sleep
import picamera
import subprocess
import bezelie
import time
from random import randint         # 乱数の発生


# 変数
#ttsFile = "/home/pi/bezelie/dev_edgar/exec_openJTalk.sh" # 発話シェルスクリプトのファイル名
ttsFile = "/home/pi/bezelie/dev_edgar/exec_talkEng.sh" # 発話シェルスクリプトのファイル名
dataFile = "/home/pi/bezelie/dev_edgar/counter.txt"               # 

# 準備
bez = bezelie.Control()               # べゼリー操作インスタンスの生成
bez.moveCenter()                      # サーボをセンタリング
sleep(0.5)

# Settin Up
switch_pin = 4      # GPIO 4
trigger_pin = 27    # GPIO 27
echo_pin = 22       # GPIO 22
actionDistance = 10 # centi mater
GPIO.setmode(GPIO.BCM)
GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)
GPIO.setup(switch_pin, GPIO.IN)                # GPIOを入力モードに設定
switch = "on"
photoNo = 1         # jpg File Number

# Function
def readFile():                # デバッグファイル出力機能
  f = open (dataFile,'r')
  textBefore = ""
  for row in f:
    textBefore = textBefore + row
  f.close()
  return textBefore

def writeFile(text):                # デバッグファイル出力機能
  f = open (dataFile,'w')
  f.write(text + "\n")
  f.close()

def send_trigger_pulse():
    GPIO.output(trigger_pin, True)
    sleep(0.0001)
    GPIO.output(trigger_pin, False)

def wait_for_echo(value, timeout):
    count = timeout
    while GPIO.input(echo_pin) != value and count > 0:
        count -= 1

def get_distance():
    send_trigger_pulse()
    wait_for_echo(True, 10000)
    start = time.time()
    wait_for_echo(False, 10000)
    finish = time.time()
    pulse_len = finish - start
    distance  = pulse_len / 0.000058
    return (distance)

def sensorCheck():
    global runNo
    global photoNo
    if get_distance() < actionDistance:
      bez.moveCenter()
      #subprocess.call("sh "+ttsFile+" "+"こんにちわ", shell=True)
      subprocess.call("sh "+ttsFile+" "+"Smile", shell=True)
#      camera.stop_preview()
      camera.capture('/home/pi/Pictures/'+ str(runNo) +"-"+ str(photoNo) +'.jpg')
      photoNo += 1
#      camera.start_preview()
      sleep(0.5)

# get runNo
t = readFile()
runNo = int(t)+1
writeFile(str(runNo))
print "runNo= "+str(runNo)

# Main Loop
try:
  with picamera.PiCamera() as camera:
    camera.resolution = (320, 240)   # Change this number for your display
    camera.rotation = 180            # comment out if your screen upside down
#    camera.start_preview()
#    sleep(2)
    while (True):
      if GPIO.input(switch_pin)==GPIO.HIGH:
        if switch == "on":
          switch = "off"
        else:
          switch = "on"
        sleep (1)
      else:
        if switch == "on":
          sensorCheck()
          r = randint(1,8)
          if r < 3:
            r = randint(1,4)
            if r < 2:
              bez.moveHead(-10)
              sleep (0.5)
              bez.moveHead(0)
            elif r < 3:
              bez.moveHead(10)
              sleep (0.5)
              bez.moveHead(0)
            else:
              bez.moveHead(-10)
              sleep (0.5)
              bez.moveHead(10)
              sleep (0.5)
              bez.moveHead(0)
          elif r < 5:
            r = randint(1,4)
            if r < 2:
              bez.moveBack(-10)
              sleep (0.5)
              bez.moveBack(0)
            elif r < 3:
              bez.moveBack(10)
              sleep (0.5)
              bez.moveBack(0)
            else:
              bez.moveBack(10)
              sleep (0.5)
              bez.moveBack(-10)
              sleep (0.5)
              bez.moveBack(0)
          elif r < 7:
            r = randint(1,4)
            if r < 2:
              bez.moveStage(-20)
            elif r < 3:
              bez.moveStage(-10)
            else:
              bez.moveStage(10)
          else:
            sleep (1)
          sleep (0.5)
        else:
          sleep (1)

except KeyboardInterrupt:
  print " Interrupted by Keyboard"

GPIO.cleanup()
