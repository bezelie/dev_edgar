# -*- coding: utf-8 -*-
# 音声対話デモ
# for Bezelie Edgar
# for Raspberry Pi
# by Jun Toyoda (Team Bezelie)
# from Aug15th2017

from time import sleep             # ウェイト処理
import subprocess                  #
import socket                      # ソケット通信モジュール
import xml.etree.ElementTree as ET # XMLエレメンタルツリー変換モジュール


# Variables
muteTime = 0.5    # 音声入力を無視する時間
bufferSize = 512  # 受信するデータの最大バイト数。できるだけ小さな２の倍数が望 $
ttsFile  = "exec_openJTalk.sh"  # 音声合成

# TCPクライアントを作成しJuliusサーバーに接続する
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(('10.0.0.1', 10500))  # Juliusサーバーに接続
client.connect(('localhost', 10500))  # Juliusサーバーに接続

# Set up
subprocess.call('amixer cset numid=1 100% -c 0', shell=True)       # スピーカー音量
subprocess.call('sudo amixer sset Mic 50 -c 0 -q', shell=True) # マイク感受性

# Main Loop
def main():
  try:
    data = ""
    print "起動"
    subprocess.call("sh "+ttsFile+" "+"起動完了", shell=True)
    while True:
      if "</RECOGOUT>\n." in data:  # RECOGOUTツリーの最終行を見つけたら以下の処理を行う
        try:
          data = data[data.find("<RECOGOUT>"):].replace("\n.", "")
          root = ET.fromstring('<?xml version="1.0" encoding="utf-8" ?>\n' + data)
          print root
          keyWord = ""
          for whypo in root.findall("./SHYPO/WHYPO"):
            keyWord = keyWord + whypo.get("WORD")
          print keyWord
        except:
          print "------------------------"
        data = ""  # 認識終了したのでデータをリセットする
      else:
        data = data + client.recv(bufferSize)  # Juliusサーバーから受信
  except KeyboardInterrupt: # CTRL+Cで終了
    print "  終了しました"
    client.close()

if __name__ == "__main__":
#    pass
    main()
