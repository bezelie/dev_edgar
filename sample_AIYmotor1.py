#!/usr/bin/env python3

import sys
import aiy.audio
import aiy.cloudspeech
import aiy.voicehat
from time import sleep
from gpiozero import PWMOutputDevice
from gpiozero import Servo

adj0=-0.05
adj1=0
adj2=0
max0=(2.0+adj0)/1000
min0=(1.0+adj0)/1000
max1=(2.0+adj1)/1000
min1=(1.0+adj1)/1000
max2=(2.0+adj2)/1000
min2=(1.0+adj2)/1000

servo0 = Servo(26,min_pulse_width=min0,max_pulse_width=max0)
servo1 = Servo(6,min_pulse_width=min1,max_pulse_width=max1)
servo2 = Servo(13,min_pulse_width=min2,max_pulse_width=max2)
servo0.value=None
servo1.value=None
servo2.value=None

# 変数
motorL = PWMOutputDevice(4)
motorR = PWMOutputDevice(17)

# 準備

def main():
    aiy.audio.say("here we go!")
    recognizer = aiy.cloudspeech.get_recognizer()
    recognizer.expect_phrase('go straight')
    recognizer.expect_phrase('stop')
    recognizer.expect_phrase('turn right')
    recognizer.expect_phrase('turn left')
    recognizer.expect_phrase('good bye')

    aiy.audio.get_recorder().start()

    while True:
        servo0.value=None
        servo1.value=None
        servo2.value=None
        sleep (0.5)
        print('Listening...')
        text = recognizer.recognize()
        if text is None:
            print('Sorry, I did not hear you.')
            aiy.audio.say("hm")
        else:
            print('You said "', text, '"')
            if 'go straight' in text:
                aiy.audio.say("straight")
                servo2.value=-0.5
                motorL.on()
                motorR.on()
                sleep(0.5)
                motorL.off()
                motorR.off()
                servo2.value=0
                sleep(0.5)
            elif 'stop' in text:
                aiy.audio.say("stop")
                motorL.off()
                motorR.off()
            elif 'turn right' in text:
                aiy.audio.say("right")
                servo0.value=-0.5
                motorR.on()
                sleep(0.25)
                motorR.off()
                sleep(0.5)
                servo0.value=0
                sleep(0.5)
            elif 'turn left' in text:
                aiy.audio.say("left")
                servo0.value=0.5
                motorL.on()
                sleep(0.25)
                motorL.off()
                sleep(0.5)
                servo0.value=0
                sleep(0.5)
            elif 'goodbye' in text:
                aiy.audio.say("see you soon")
                sleep(1)
                exit (0)
            else:
                aiy.audio.say("Sorry, I could not hear you")
                sleep(1)

if __name__ == '__main__':
    button = aiy.voicehat.get_button()
    aiy.audio.say("press the button and speak")
    print('Press the button, and speak')
    servo1.value=-0.5
    sleep (0.5)
    servo1.value=0.5
    sleep (0.5)
    servo1.value=0
    sleep (0.5)
    button.wait_for_press()
    main()
