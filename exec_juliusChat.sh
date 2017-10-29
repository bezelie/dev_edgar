# Julius 起動スクリプト
ALSADEV="plughw:0,0" julius -w /home/pi/bezelie/dev_edgar/chatEntity.dic -C /home/pi/bezelie/dev_edgar/julius.jconf -module > /dev/null &
# ALSADEV="plughw:0,0" julius -w chatEntity.dic -C julius.jconf -module > /dev/null &
echo "Julius's Process ID = "$!
# -moduleオプション= Juliusをモジュールモードで起動
# /dev/nullはlinuxの特殊ファイルで、何も出力したくない時に指定する。
# $! = シェルが最後に実行したバックグラウンドプロセスのID
# juliusが立ち上がる前にアクセスしようとするとエラーになるので数秒待つ
