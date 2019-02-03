#!/usr/bin/python
# -*- coding: utf-8 -*-
# Bezelie Sample Code for Raspberry Pi : 発話するサンプル
# スピーカーなどを接続してから試してください。

# ライブラリの読み込み
from time import sleep                # ウェイト処理
import subprocess                     # 外部プロセスを実行するモジュール

# メインループ
def main():
  try:
    while (True):
      subprocess.call("aplay -l", shell=True)
      subprocess.call("aplay -D plughw:0,0 Front_Center.wav", shell=True)
      sleep(0.5)
  except KeyboardInterrupt:
    print ' 終了しました'

if __name__ == "__main__":
    main()
