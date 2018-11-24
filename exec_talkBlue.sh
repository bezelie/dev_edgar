#!/bin/bash
# 音声合成（Open JTalk）起動スクリプト
HTSVOICE=/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice
#HTSVOICE=/usr/share/hts-voice/htsvoice-tohoku-f01/tohoku-f01-neutral.htsvoice
# angry, happy, neutral, sad
# HTSVOICE=/usr/share/hts-voice/mei/mei_happy.htsvoice
# angry, happy, normal, sad
DICDIRE=/var/lib/mecab/dic/open-jtalk/naist-jdic/
VOICEDATA=/tmp/voice.wav
sudo echo "$1" | open_jtalk \
-x $DICDIRE \
-m $HTSVOICE \
-ow $VOICEDATA \
-s 50000 \
-b 0.0 \
-r 1.5 \
-fm 0.0 \
-u 0.0 \
-jm 1.0 \
-jf 0.2 \
-z 10000 \

# s   サンプリング周波数　1-
#     0000-
#-p 80 \
# p   フレーム周期 1-
#     100ぐらいか。大きな値にすると実行に時間がかかってしまう。
#-a 0.05 \
# a   オールパス値　0.0-1.0
# b   ポストフィルター係数 0.0-1.0
# r   スピーチ速度係数 0.0-(1.0)-
#     1.5ぐらいがよいかな。大きくても2.5ぐらいか。大きいと冒頭が切れる。
# fm  追加ハーフトーン (0.0)
# u   有声・無声境界値 0.0-(0.5)-1.0
# jm  スペクトラム係数内変動の重み 0.0-(1.0)-
# jf  F0系列内変動の重み 0.0-(1.0)-
#     0にすると平坦なロボット声になる。
# z   オーディオバッファサイズ 0-(0)-

amixer cset numid=1 100%
#aplay -q -D plughw:2,0 $VOICEDATA
#aplay -D plughw:0,1 $VOICEDATA
#sudo rm -f $VOICEDATA
