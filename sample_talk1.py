# -*- coding: utf-8 -*-
# Bezelie Sample Code for Raspberry Pi : 発話するサンプル

# ライブラリの読み込み
import subprocess                     # shellの実行をするためのライブラリ
from time import sleep                # ウェイト処理
import bezelie                        # べゼリー専用モジュール

openJTalkFile = "exec_openJTalk.sh"   # 発話シェルスクリプトのファイル名

# Setting
bez = bezelie.Control()               # べゼリー操作インスタンスの生成
bez.setTrim(head=0, back=-5, stage=0) # センター位置の微調整
bez.moveCenters()                     # サーボのセンタリング

# Main Loop
def main():
  try:
    while (True):
      subprocess.call("sh "+openJTalkFile+" "+"こんにちわ", shell=True)
      sleep(0.5)
  except KeyboardInterrupt:
    print ' Interrupted by Keyboard'

if __name__ == "__main__":
    main()
