#!/usr/bin/env python3

from time import sleep
from gpiozero import PWMOutputDevice

pwm = PWMOutputDevice(17)

def main():
  while True:
    pwm.on()
    sleep (1)
    pwm.off()
    sleep (1)

if __name__ == '__main__':
    main()
