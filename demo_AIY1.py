#!/usr/bin/env python3

import sys
import aiy.audio
import aiy.cloudspeech
import aiy.voicehat
from time import sleep
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

def main():
    aiy.audio.say("hi there")
    recognizer = aiy.cloudspeech.get_recognizer()
    recognizer.expect_phrase('hello')
    recognizer.expect_phrase('what is your name')
    recognizer.expect_phrase('how are you')
    recognizer.expect_phrase('good bye')

    button = aiy.voicehat.get_button()
    aiy.audio.get_recorder().start()

    aiy.audio.say("press the button and speak")
    while True:
        servo0.value=None
        servo1.value=None
        servo2.value=None
        print('Press the button, and speak')
        button.wait_for_press()
        print('Listening...')
        text = recognizer.recognize()
        if text is None:
            print('Sorry, I did not hear you.')
            aiy.audio.say("hmmm")
        else:
            print('You said "', text, '"')
            if 'hello' in text:
                servo2.value=-0.5
                aiy.audio.say("hi guys")
                servo2.value=0
                sleep(1)
            elif 'what is your name' in text:
                servo2.value=0.5
                aiy.audio.say("I am Bezelie")
                servo2.value=0
                sleep(1)
            elif 'how are you' in text:
                servo0.value=0.5
                aiy.audio.say("not bad")
                servo0.value=-0.5
                aiy.audio.say("thank you")
                servo0.value=0
                sleep(1)
            elif 'goodbye' in text:
                servo2.value=-0.5
                aiy.audio.say("see you soon")
                servo2.value=0
                sleep(1)
                exit (0)
            else:
                servo1.value=0.5
                aiy.audio.say("Sorry, I can not understand you")
                servo1.value=0
                sleep(1)

if __name__ == '__main__':
    main()
