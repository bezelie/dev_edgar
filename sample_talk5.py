#!/usr/bin/python
# -*- coding: utf-8 -*-
# Bezelie Sample Code for Raspberry Pi : 発話するサンプル
# スピーカーなどを接続してから試してください。

# ライブラリの読み込み
from time import sleep                # ウェイト処理
import subprocess                     # 外部プロセスを実行するモジュール

# 変数
ttsRed = "/home/pi/bezelie/dev_edgar/exec_talkRed.sh" # 発話シェルスクリプトのファイル名
ttsBlue = "/home/pi/bezelie/dev_edgar/exec_talkBlue.sh" # 発話シェルスクリプトのファイル名
ttsGreen = "/home/pi/bezelie/dev_edgar/exec_talkGreen.sh" # 発話シェルスクリプトのファイル名
ttsPink = "/home/pi/bezelie/dev_edgar/exec_talkPink.sh" # 発話シェルスクリプトのファイル名
ttsYellow = "/home/pi/bezelie/dev_edgar/exec_talkYellow.sh" # 発話シェルスクリプトのファイル名

# メインループ
def main():
  try:
    while (True):
      subprocess.call("sh "+ttsRed+" "+"僕はべゼリーレッド", shell=True)
      subprocess.call("sh "+ttsBlue+" "+"俺はべゼリーブルーだ", shell=True)
      subprocess.call("sh "+ttsGreen+" "+"俺はべゼリーグリーン", shell=True)
      subprocess.call("sh "+ttsPink+" "+"私はべゼリーピンク", shell=True)
      subprocess.call("sh "+ttsYellow+" "+"私はべゼリーイエローよ", shell=True)
#      subprocess.call('flite -voice "kal16" -t "Hello World!"', shell=True) # English
       # Other English Voices :kal awb_time kal16 awb rms slt
      sleep(0.5)
  except KeyboardInterrupt:
    print ' 終了しました'

if __name__ == "__main__":
    main()
