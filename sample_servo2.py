#!/usr/bin/python
# -*- coding: utf-8 -*-
# Bezelie Sample Code for Raspberry Pi : べゼリーの基本アクション
# ラズパイにサーボドライバーとサーボを接続してから実行してください。

# ライブラリの読み込み
from time import sleep                # ウェイト処理
import bezelie                        # べゼリー専用モジュール

# 準備
bez = bezelie.Control()               # べゼリー操作インスタンスの生成
bez.moveCenter()                      # サーボをセンタリング
sleep(0.5)

# メインループ
def main():
  try:
    print "開始します"
    while True:
      print "happy"
      bez.moveAct('happy')            # しあわせ
      sleep (0.5)
      bez.stop()
      print "nod"
      bez.moveAct('nod')              # うなづき
      sleep (0.5)
      bez.stop()
      print "why"
      bez.moveAct('why')              # 首かしげ
      sleep (0.5)
      bez.stop()
      print "around"
      bez.moveAct('around')           # 見回し
      sleep (0.5)
      bez.stop()
      print "up"
      bez.moveAct('up')               # 見上げ
      sleep (0.5)
      bez.stop()
      print "wave"
      bez.moveAct('wave')             # くねくね
      sleep (0.5)
      bez.stop()
      print "etc"
      bez.moveAct('etc')              # ETC
      sleep (0.5)
      bez.stop()
  except KeyboardInterrupt:
    print "  終了しました"

if __name__ == "__main__":
    main()
