#!/bin/bash

# 音声合成で生成されたファイル
VOICE_FILE=/tmp/voice_${RANDOM}.wav

# 音声合成に使う音響モデル
cd $HOME/hts_voice

# make voice file
echo "$1" | $HOME/open_jtalk/bin/open_jtalk \
-m $HOME/hts_voice/nitech_jp_atr503_m001.htsvoice \
-x $HOME/open_jtalk/dic \
-g 1 \
-ow $VOICE_FILE && \

# play voice
aplay --quiet $VOICE_FILE

# delete voice 
rm -f $VOICE_FILE
