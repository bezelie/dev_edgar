#!/usr/bin/python
# -*- coding: utf-8 -*-
# Bezelie Sample Code for Raspberry Pi : サーボ動作サンプル
# ラズパイにサーボドライバーとサーボを接続してから実行してください。

# ライブラリの読み込み
from time import sleep                # ウェイト処理
import module_theater                        # べゼリー専用モジュール
import sys

# Setting
bez = module_theater.Control()               # べゼリー操作インスタンスの生成
bez.moveCenter()                     # ０番から７番までのサーボをセンタリング
sleep(0.5)

# Main Loop
def main():
  try:
    print "開始します"
    i = 1
    while i < 6:
      bez.moveHead(i, 40)
      sleep(1)
      bez.moveHead(i, 0)
      sleep(1)
      bez.moveHead(i, -40)
      sleep(1)
      bez.moveHead(i, 0)
      sleep(1)
      bez.moveBack(i, 40)
      sleep(1)
      bez.moveBack(i, 0)
      sleep(1)
      bez.moveBack(i, -40)
      sleep(1)
      bez.moveBack(i, 0)
      sleep(1)
      bez.moveStage(i, 40)
      sleep(1)
      bez.moveStage(i, 0)
      sleep(1)
      bez.moveStage(i, -40)
      sleep(1)
      bez.moveStage(i, 0)
      sleep(1)
      i = i + 1
      sleep(1)
  except KeyboardInterrupt:
    print "  終了しました"
    sys.exit(0)

if __name__ == "__main__":
    main()
