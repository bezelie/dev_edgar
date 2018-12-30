# -*- coding: utf-8 -*-
# Bezelie demo Code for Raspberry Pi : Camera and Range Sensor

import RPi.GPIO as GPIO
from time import sleep
import picamera
import subprocess
import bezelie
import time

# 変数
#ttsFile = "/home/pi/bezelie/dev_edgar/exec_openJTalk.sh" # 発話シェルスクリプトのファイル名
ttsFile = "/home/pi/bezelie/dev_edgar/exec_talkEng.sh" # 発話シェルスクリプトのファイル名

# 準備
bez = bezelie.Control()               # べゼリー操作インスタンスの生成
bez.moveCenter()                      # サーボをセンタリング
sleep(0.5)

# Settin Up
trigger_pin = 27    # GPIO 27
echo_pin = 22       # GPIO 22
actionDistance = 10 # centi mater
GPIO.setmode(GPIO.BCM)
GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)
photoNo = 1         # jpg File Number

# Function
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
    global photoNo
    if get_distance() < actionDistance:
      bez.moveCenter()
      #subprocess.call("sh "+ttsFile+" "+"こんにちわ", shell=True)
      subprocess.call("sh "+ttsFile+" "+"Smile", shell=True)
      camera.stop_preview()
      camera.capture('/home/pi/Pictures/image'+ str(photoNo) +'.jpg')
      photoNo += 1
      camera.start_preview()
      sleep(0.5)

# Main Loop
try:
  with picamera.PiCamera() as camera:
    camera.resolution = (320, 240)   # Change this number for your display
    camera.rotation = 180            # comment out if your screen upside down
    camera.start_preview()
    sleep(2)
    head = 0
    while (True):
      bez.moveBack (15)
      bez.moveStage (40, 2)
      sensorCheck()
      sleep (0.5)
      bez.moveBack (-15)
      bez.moveStage (-40, 2)
      sensorCheck()
      sleep (0.5)
      head += 10
      if head > 10:
        head = -10
      bez.moveHead (head)
      sleep (0.5)

except KeyboardInterrupt:
  print " Interrupted by Keyboard"

GPIO.cleanup()
