#!/usr/bin/python
# -*- coding: utf-8 -*-
#
from time import sleep
import json                        # jsonファイルを扱うモジュール

# 変数
scenarioFile = "/home/pi/bezelie/dev_edgar/scenario.json"        # 設定ファイル

# メインループ
def main():
  try:
    print "開始します"
    f = open (scenarioFile,'r')
    data = json.load(f)
    num = int(data['scene0'][1]['num'])    #
    name = (data['scene0'][1]['name'])    #
    print num
    print name
  except KeyboardInterrupt:
    print ' 終了しました'
if __name__ == "__main__":
    main()
