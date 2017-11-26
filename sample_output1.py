# -*- coding: utf-8 -*-                : 文字コードの指定
# Bezelie Sample Code for Raspberry Pi : outputのサンプル
# 

# ライブラリの読み込み
from time import sleep                 # sleep(ウェイト処理)ライブラリの読み込み
import RPi.GPIO as GPIO                # GPIO(汎用入出力端子)ライブラリの読み込み

# 初期設定
GPIO.setmode(GPIO.BCM)                 # GPIOをGPIO番号で指定できるように設定
GPIO.setup(27, GPIO.OUT)                # GPIOの27ピンをoutputモードに設定

# 関数
def main():
  try:
    print "開始します"
    while True:                        # 繰り返し処理
      GPIO.output(27, True)
      sleep (1)
      GPIO.output(27, False)
      sleep (1)
  except KeyboardInterrupt:            # コントロール＋Cが押された場合の処理
    print "終了しました"

# 直接実行された場合の処理
if __name__ == "__main__":
    main()
