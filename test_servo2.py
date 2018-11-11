#!/usr/bin/python
# -*- coding: utf-8 -*-
# Bezelie Sample Code for Raspberry Pi : サーボ動作サンプル
# ラズパイにサーボドライバーとサーボを接続してから実行してください。

# ライブラリの読み込み
from time import sleep                # ウェイト処理
import flitz                          # べゼリー専用モジュール
import sys

# Setting
bez = flitz.Control()               # べゼリー操作インスタンスの生成
bez.moveCenter()                     # ０番から７番までのサーボをセンタリング
sleep(0.5)

# Main Loop
def main():
  try:
    print "開始します"
    while True:
      bez.act(5, "rollRightLeft")
      bez.stop()
      sleep(1)
  except KeyboardInterrupt:
    print "  終了しました"
    sys.exit(0)

if __name__ == "__main__":
    main()
