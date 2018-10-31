#!/bin/bash
# Julius（キーワード認識版）をモジュールモードで起動
# ALSADEV="plughw:0,0" /usr/local/bin/julius -w /home/pi/bezelie/chatEntity.dic -C /home/pi/bezelie/dev_edgar/julius.jconf -module &
/usr/local/bin/julius -w /home/pi/bezelie/chatEntity.dic -C /home/pi/bezelie/dev_edgar/julius.jconf -module &
echo "Julius's Process ID = "$!
# /dev/nullはlinuxの特殊ファイルで、何も出力したくない時に指定する。
# $! = シェルが最後に実行したバックグラウンドプロセスのID
exit 0
