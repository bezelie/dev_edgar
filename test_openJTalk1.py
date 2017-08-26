# -*- coding: utf-8 -*-

from time import sleep             # ウェイト処理
import subprocess                  #

openJTalkFile = "/home/pi/bezelie/dev_edgar/exec_openJTalk.sh"  #

subprocess.call("sh "+openJTalkFile+" "+"起動します", shell=True)
