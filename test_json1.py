#!/usr/bin/python
# -*- coding: utf-8 -*-
#
from time import sleep
import json                        # jsonファイルを扱うモジュール

# 変数
file = "/home/pi/bezelie/dev_edgar/trim.json"        # 設定ファイル

# メインループ
def main():
  try:
    print "開始します"
    f = open (file,'r')
    data = json.load(f)
    n=1
    head = int(data['data'+str(n)][0]['head'])    #
    back = int(data['data'+str(n)][0]['back'])    #
    print head
    print back
  except KeyboardInterrupt:
    print ' 終了しました'
if __name__ == "__main__":
    main()
