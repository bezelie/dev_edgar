#!/usr/bin/env python3
"""A demo of the Google CloudSpeech recognizer."""

import sys
import aiy.audio
import aiy.cloudspeech
import aiy.voicehat
from gpiozero import Servo
from time import sleep

myCorrection=0
maxPW=(2.0+myCorrection)/1000
minPW=(1.0+myCorrection)/1000

servo1 = Servo(26,min_pulse_width=minPW,max_pulse_width=maxPW)

def main():
    while True:
        print('Press the button and speak')
        for value in range(0,21):
            value2=(float(value)-10)/10
            servo1.value=value2
            print(value2)
            sleep(0.5)

if __name__ == '__main__':
    main()
