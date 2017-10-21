# -*- coding: utf-8 -*-
# Bezelie Sample Code for Raspberry Pi : Servo Movement Test

from time import sleep             # ウェイト処理
import bezelie                     # べゼリー専用モジュール

# Servo Setting
bez = bezelie.Control()               # べゼリー操作インスタンスの生成
bez.setTrim(head=0, back=-5, stage=0) # センター位置の微調整
bez.moveCenters()                     # ０番から７番までのサーボをセンタリング
sleep(0.5)

# Main Loop
def main():
  try:
    print "開始します"
    while True:
      bez.moveAct('happy')
      bez.stop()
      bez.moveAct('nod')
      bez.stop()
      bez.moveAct('why')
      bez.stop()
      sleep (0.5)
  except KeyboardInterrupt:
    print "  終了しました"

if __name__ == "__main__":
    main()

