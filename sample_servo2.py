# -*- coding: utf-8 -*-
# Bezelie Sample Code for Raspberry Pi : サーボ動作サンプル
# ラズパイにサーボドライバーとサーボを接続してから実行してください。

# ライブラリの読み込み
from time import sleep                # ウェイト処理
import bezelie                        # べゼリー専用モジュール

# Setting
bez = bezelie.Control()               # べゼリー操作インスタンスの生成
bez.setTrim(head=0, back=0, stage=0) # センター位置の微調整
bez.moveCenters()                     # ０番から3番までのサーボをセンタリング
sleep(0.5)

# Main Loop
def main():
  try:
    print "開始します"
    while True:
      print "happy"
      bez.moveAct('happy')            # しあわせ
      bez.stop()
      print "nod"
      bez.moveAct('nod')              # うなづき
      bez.stop()
      print "why"
      bez.moveAct('why')              # 首かしげ
      bez.stop()
      print "around"
      bez.moveAct('around')           # 見回し
      bez.stop()
      print "up"
      bez.moveAct('up')               # 見上げ
      bez.stop()
      print "wave"
      bez.moveAct('wave')             # くねくね
      bez.stop()
      print "etc"
      bez.moveAct('etc')              # ETC
      bez.stop()
      sleep (0.5)
  except KeyboardInterrupt:
    print "  終了しました"

if __name__ == "__main__":
    main()
