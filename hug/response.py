# -*- coding: utf-8 -*-


import sys

import commands

import random

import datetime

import time

import xml.etree.ElementTree as ET

import threading
import socket
import select
import json
import csv
import RPi.GPIO as GPIO

#
buffer_size = 512
VOICE_PATH = '/home/pi/hug/voice/'

RANDOM_PLAY_MODE = 10
CONVERSATION_MODE = 20

MIC_VOLUME = '5%'

MALE = 10
FEMALE = 20
speaker = FEMALE

random_voice_sequence = 1

button_request_count = 0
last_time = datetime.datetime.now()
button_push_count = 0

JTALK_PATH = '/home/pi/hug/bin/jtalk.sh'

is_playing = 0

# GPIO Setting
GPIO.setmode(GPIO.BCM)
#GPIO.cleanup()
GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.IN)
# GPIO Setting (LED)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)

result = commands.getoutput('env')
print result

# Mic Setting
commands.getoutput('sudo amixer -q sset Mic ' + MIC_VOLUME + ' -c 0')

# connect julius
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.settimeout(300)
enabled_julius = False
for count in range(10):
  try:
    client.connect(('localhost', 10500))
    enabled_julius = True
    break
  except socket.error, e:
    print 'failed socket connect. retry\n'
    time.sleep(2)

if enabled_julius == False:
  print 'boot failed...\n'
  commands.getoutput(JTALK_PATH + ' 起動に失敗しました。機器を再起動してください。')
  sys.exit(1)

def get_random_voice_num():

  global random_voice_sequence

  if random_voice_sequence == 1:
    # 肩揉み
    voice_num = 34
  else:
    voice_num = random.randint(1,50)

  random_voice_sequence = random_voice_sequence + 1
  if random_voice_sequence > 3:
    random_voice_sequence = 1

  return voice_num

def play_random_voice():
  voice_num = get_random_voice_num()
  result = commands.getoutput('aplay -Dplug:default '
                              + VOICE_PATH
                              + str(speaker)
                              + '/'
                              + str(voice_num)
                              + '.wav')

def play_voice(word):
  result = ''
  voice_num = 0
  if word == u'こんにちは':
    voice_num = 1

  elif word == u'聞えますか':
    voice_num = random.randint(2,3)

  elif word == u'今何時':
    tmp_num = random.randint(1,2)
    if tmp_num == 1:
      voice_num = 4
    else:
      voice_num = 6

  elif word == u'今日の天気':
    voice_num = 5

  elif word == u'おはよう':
    voice_num = random.randint(7,9)

  elif word == u'おやすみ':
    voice_num = 10

  elif word == u'ただいま':
    voice_num = random.randint(11,13)

  elif word == u'いってきます':
    voice_num = 14

  elif word == u'ハグ':
    voice_num = random.randint(15,16)

  elif word == u'ありがとう':
    voice_num = 17

  elif word == u'ごめんなさい':
    voice_num = 18

  elif word == u'疲れてる':
    voice_num = 19

  elif word == u'どうしたの':
    voice_num = random.randint(20,22)

  elif word == u'予定':
    voice_num = 23

  elif word == u'私のこと':
    voice_num = random.randint(24,25)

  elif word == u'私頑張ってる':
    voice_num = random.randint(26,27)

  elif word == u'好きだよ':
    voice_num = random.randint(28,29)

  elif word == u'かわいいね':
    voice_num = random.randint(30,31)

  elif word == u'抱きしめて':
    voice_num = random.randint(32,33)

  elif word == u'肩揉んで':
    voice_num = 34

  elif word == u'疲れた':
    voice_num = random.randint(35,37)

  elif word == u'寂しいな':
    voice_num = random.randint(38,40)

  elif word == u'休みたい':
    voice_num = 41

  elif word == u'眠い':
    voice_num = 42

  elif word == u'あぁぁ':
    voice_num = random.randint(43,44)

  elif word == u'おぉぉ':
    voice_num = random.randint(45,46)

  else:
    debug_message('no match\n')
    voice_num = random.randint(47,50)

  # mute mic
  commands.getoutput('sudo amixer -q sset Mic 0 -c 0')
  is_playing = True

  # play voice
  debug_message('play voice number ' + str(voice_num) + '\n')
  result = commands.getoutput('aplay -Dplug:default '
                              + VOICE_PATH
                              + str(speaker)
                              + '/'
                              + str(voice_num)
                              + '.wav')
  debug_message('play voice result : ' + result)

  # mic on
  commands.getoutput('sudo amixer -q sset Mic ' + MIC_VOLUME + ' -c 0')
  is_playing = False

def random_play_mode_loop():

  debug_message('random play mode loop\n')
  commands.getoutput(JTALK_PATH + ' ランダムモードを起動しました')

  try:
    # check request change speaker
    set_keep_press_button_checker()

    while True:
      try:
        debug_message('loop while\n')

        if GPIO.input(23) == GPIO.LOW:
          play_random_voice()
        time.sleep(1)
      except:
        debug_message('except error\n')
        import traceback
        traceback.print_exc()

  except KeyboardInterrupt:
    debug_message('stop process CTRL+C\n')
    client.close()
    sys.exit(0)

def check_keep_press_button():
  global button_push_count
  if GPIO.input(24) == GPIO.LOW:
    button_push_count = button_push_count + 1
    if button_push_count >= 3:
      button_push_count = 3
  else:
    button_push_count = 0
  debug_message('button_push_count = ' + str(button_push_count) + '\n') 
  if button_push_count >= 3:
    check_change_speaker()
  # ボタンが押し続けられているかの監視の再開  
  set_keep_press_button_checker()

def check_change_speaker():
  debug_message('check_change_speaker\n')
  if GPIO.input(23)==GPIO.LOW:
    change_speaker()
    global button_push_count
    button_push_count = 0

def set_speaker_led():
  global speaker
  global MALE
  global FEMALE
  if speaker == MALE:
    GPIO.output(2, False)
    GPIO.output(3, False)
    GPIO.output(4, True)
  else:
    GPIO.output(2, True)
    GPIO.output(3, False)
    GPIO.output(4, False)

def change_speaker():
  global speaker
  global MALE
  global FEMALE
  if speaker == MALE:
    speaker = FEMALE
    set_speaker_led()
    commands.getoutput(JTALK_PATH + ' 女性に切り替えました')
  else:
    speaker = MALE
    set_speaker_led()
    commands.getoutput(JTALK_PATH + ' 男性に切り替えました')
  debug_message('speaker ' + str(speaker))

def set_keep_press_button_checker():
  t = threading.Timer(1, check_keep_press_button)
  t.setDaemon(True)
  t.start()

def socket_buffer_clear():

  # buffer clear
  while True:
    rlist, _, _ = select.select([client], [], [], 1)

    if len(rlist) > 0: 
      dummy_buffer = client.recv(buffer_size)
    else:
      break

def parse_recogout(stt):

  # トークボタンが押されていない時は認識結果は破棄する
  if GPIO.input(23) != GPIO.LOW:
  
    socket_buffer_clear()

  else:

    try:
      stt = stt[stt.find("<RECOGOUT>"):].replace("\n.", "")
      root = ET.fromstring('<?xml version="1.0" encoding="utf-8" ?>\n' + stt)
  
      keyword = ""
      for whypo in root.findall("./SHYPO/WHYPO"):
        keyword = keyword + whypo.get("WORD")
      debug_message('keyword = ' + keyword + '\n')
  
      if not is_playing:
        play_voice(keyword)
        socket_buffer_clear()
  
      else:
        debug_message('skip play voice\n')
  
    except:
      debug_message('stt parse error\n')
      import traceback
      traceback.print_exc()

def conversation_mode_loop():

  debug_message('conversation mode loop\n')
  commands.getoutput(JTALK_PATH + ' 会話モードを起動しました')

  try:
    # check request change speaker
    set_keep_press_button_checker()

    stt = ""
    while True:
      debug_message('loop while\n')
      # recieve julius speak to text
      if "</RECOGOUT>\n." in stt:

        parse_recogout(stt)
        stt = ""

      else:
        stt = stt + client.recv(buffer_size)
        debug_message('stt = ' + stt + '\n')

  except KeyboardInterrupt:
    debug_message('stop process CTRL+C\n')
    client.close()
    sys.exit(0)

def check_speaker():
  debug_message('check speaker\n')

def check_mode():
  debug_message('check mode\n')
  if GPIO.input(24) == GPIO.LOW:
    return RANDOM_PLAY_MODE
  return CONVERSATION_MODE

def set_play_bgm():
  d = threading.Thread(name = 'loop_bgm', target = loop_bgm)
  #d.setDaemon(True)
  d.start()

def loop_bgm():
  try:
    while True:
      result = commands.getoutput('aplay ' + VOICE_PATH + str(speaker) + '/' + 'bgm.wav')

  except KeyboardInterrupt:
    debug_message('stop process CTRL+C\n')
    sys.exit(0)

def main():
  debug_message('start main\n')

  # Speaker LED Setting
  set_speaker_led()

  mode = check_mode()
  if mode == RANDOM_PLAY_MODE:
    random_play_mode_loop()
  else:
    #set_play_bgm()
    conversation_mode_loop()

def debug_message(message):
  #sys.stdout.write(message)
  return

if __name__ == "__main__":
  main()
  debug_message('end\n')
  sys.exit(0)

