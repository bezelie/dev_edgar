#!/usr/bin/python
# -*- coding: utf-8 -*-
# Bezelie Sample Code for Raspberry Pi : サーボを個別に動かす
# ラズパイにサーボドライバーとサーボを接続してから実行してください。

# ライブラリの読み込み
from time import sleep                # ウェイト処理
import bezelie                        # べゼリー専用モジュール

# 定数
headMiddle = 10
headMax = headMiddle + 30
headMin = headMiddle - 10
backMiddle = 5
backMax = backMiddle + 20
backMin = backMiddle - 15
stageMiddle = 0
stageMax = stageMiddle + 40
stageMin = stageMiddle - 35

# 準備
bez = bezelie.Control()               # べゼリー操作インスタンスの生成
#bez.moveCenter()                      # サーボをセンタリング
bez.moveHead(headMiddle)                 # 頭の上下
bez.moveBack(backMiddle)                 # 頭の左右
bez.moveStage(stageMiddle)                # 体の左右
sleep(0.5)

# メインループ
def main():
  try:
    print "開始します"
    while True:
      print "Head 上回転"
      bez.moveHead(headMax)                # 頭の上下
      sleep (0.5)
      print "Head 下回転"
      bez.moveHead(headMin)               # 頭の上下
      sleep (0.5)
      print "Head 中央"
      bez.moveHead(headMiddle)                 # 頭の上下
      sleep (1)
      print "Back 右回転"
      bez.moveBack(backMax)                # 頭の左右
      sleep (0.5)
      print "Back 左回転"
      bez.moveBack(backMin)               # 頭の左右
      sleep (0.5)
      print "Back 中央"
      bez.moveBack(backMiddle)                 # 頭の左右
      sleep (1)
      print "Stage 右回転"
      bez.moveStage(stageMax)               # 体の左右
      sleep (0.5)
      print "Stage 左回転"
      bez.moveStage(stageMin)              # 体の左右
      sleep (0.5)
      print "Stage 中央"
      bez.moveStage(stageMiddle)                # 体の左右
      sleep (1)
  except KeyboardInterrupt:
    print "  終了しました"

if __name__ == "__main__":
    main()
