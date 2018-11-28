#!/usr/bin/python
# -*- coding: utf-8 -*-
# Bezelie Sample Code for Raspberry Pi : LEDを明滅させる
# ラズパイにサーボドライバーとLEDを接続してから実行してください。

# ライブラリの読み込み
from time import sleep                # ウェイト処理
import bezelie                        # べゼリー専用モジュール

# 準備
bez = bezelie.Control()               # べゼリー操作インスタンスの生成

# メインループ
def main():
  try:
    print "開始します"
    while True:
      bez.onLed(3)                    # 3番のLEDを点灯
      sleep (0.5)
      bez.offLed(3)                   # 3番のLEDを消灯
      sleep (0.5)
  except KeyboardInterrupt:
    print "  終了しました"

if __name__ == "__main__":
    main()
