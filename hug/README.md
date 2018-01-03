# HUG Huptic Utility Guardian (ネックピロースピーカー) 

## 動作環境

  - Raspberry Pi 3 Model B
  - SD CARD 8GB以上
  - USBマイク
  - イヤホンジャックに繋がるスピーカー
  - Raspbian GNU/Linux 9.1 (stretch)

## OSのインストール

  - Raspbianのダウンロード
    - Downloads
      - https://www.raspberrypi.org/downloads/
        - NOOBS のZIPをローカルPCにダウンロードして解凍
  - SDカードのフォーマット
    - SD/SDHC/SDXC用SDメモリカードフォーマッター 5.0
      - https://www.sdcard.org/jp/downloads/formatter_4/
        - ダウンロードして解凍、実行し、SDカードをフォーマット
  - 解凍済みのNOOPSを丸ごとSDカードにコピー
  - Raspbianのセットアップ
    - SDカードをRaspberry Piに差して、Raspberry Piを起動
    - 画面の指示に従ってRaspbianをインストール

## マイクの設定

  - USBオーディオアダプタの優先度を最上位にする
```
1. 現在の優先度を確認
$ cat /proc/asound/modules 
  ※snd_usb_audioが 0 になっていればOK

2. (0でない場合は)下記ファイルを作成して優先度を変更する
$ sudo vi /etc/modprobe.d/alsa-base.conf
-------------------------------------------
options snd slots=snd_usb_audio,snd_bcm2835
options snd_usb_audio index=0
options snd_bcm2835 index=1
-------------------------------------------

3. Raspberry Piを再起動

4. (1)を再度実行して優先度が変わったのを確認
```

## スピーカーの設定

  - 特になし

## HUGの動作に必要な機能

  - 音声認識
    - Julius ディクテーションキット 4.4
    - HUG
  - 音声合成
    - HTS Engine Api 1.10
    - Open JTalk 1.10
    - HTS voice 1.0.5

## Julius インストール

  - ディクテーションキット 4.4 をダウンロードして解凍
    - https://osdn.net/projects/julius/releases/66544
      - 解凍後、src/以下にあるソースコードを解凍
  - ソースからコンパイルする
    - http://julius.osdn.jp/juliusbook/ja/desc_install.html#id2486460
      - ※configureにはprefixを指定すること
```
$ mkdir $HOME/julius
$ ./configure --prefix=$HOME/julius
```
  - モデルをコピー
```
1. フォルダを作成
$ mkdir -p $HOME/julius/model/lang_m $HOME/julius/model/phone_m

2. 解凍したディクテーションキット 4.4 からファイルをコピー
cd 解凍ディレクトリ
cp ./model/lang_m/bccwj.60k.htkdic $HOME/julius/model/lang_m/
cp ./model/phone_m/jnas-tri-3k16-gid.binhmm $HOME/julius/model/phone_m/
cp ./model/phone_m/logicalTri $HOME/julius/model/phone_m/
```
  - 参考
    - Julius音声認識パッケージ
      - http://julius.osdn.jp/index.php?q=dictation-kit.html

## HUG インストール

  - 任意の場所にダウンロード(仮に ~/hug にダウンロード)
```
cd ~/
git clone https://github.com/NamcoBandaiStudios/hug.git
```
  - 実行権限を付与
```
chmod u+x ~/hug/bin/*
```

## hts engine api インストール

  - 「参考」のサイトにてSorce Codeをダウンロードしてビルド&インストール
    - ビルド方法は、解凍したファイルにある INSTALL ファイルを参照
      - ※configureにはprefixを指定すること
```
$ mkdir $HOME/hts_engine
$ ./configure --prefix=$HOME/hts_engine
```
  - 参考
    - hts_engine API
      - http://hts-engine.sourceforge.net/

## open jtalk インストール

  - 「参考」のサイトにてSorce Codeをダウンロードしてビルド&インストール
    - ビルド方法は、解凍したファイルにある INSTALL ファイルを参照
      - ※configureにはprefixを指定すること
      - ※configureは --with-charset=utf-8 オプションを指定すること
```
$ mkdir $HOME/open_jtalk
$ ./configure --prefix=$HOME/open_jtalk --with-charset=UTF-8 --with-hts-engine-header-path=$HOME/hts_engine/include --with-hts-engine-library-path=$HOME/hts_engine/lib
```
  - 参考
    - Open JTalk
      - http://open-jtalk.sourceforge.net/

## hts voice (音響モデル)インストール

  - 「参考」のサイトにてBinary Packageをダウンロードして指定の場所にコピー
```
$ cd /tmp
$ wget ダウンロードURL
$ tar zxvf hts_voice_nitech_jp_atr503_m001-1.05.tar.gz
$ cd hts_voice_nitech_jp_atr503_m001-1.05
$ mkdir $HOME/hts_voice
$ cp nitech_jp_atr503_m001.htsvoice $HOME/hts_voice
```
  - 参考
    - Open JTalk
      - http://open-jtalk.sourceforge.net/

## 使用時の留意点

  - トークボタン
    - ボタンが反応するのは話し終えた直後なため、話を終えたと同時にトークボタンを離すと会話を認識しない場合がある
    - 理由: juliusは認識が完了しないと何も返さないので、会話中という状態をpythonスクリプト側で判断できないため、会話認識結果がjuliusから取得した時に、トークボタンが押されていたら、会話認識結果を使い、そうでない場合は、会話認識結果を破棄するという仕組みとしてある
  - 雑音対策
    - juliusのオプション -zmean を有効にして、入力した音声に対して直流成分除去を行っている
    - 仕組みとしては「Julius起動後，無音を含めた最初の 48,000 サンプル分の振幅平均を直流成分（オフセット）として以降の入力の直流成分除去を行う」となっている為、マイクのサンプリングが48,000に達するまでは、会話をしてはいけない。会話をしてしまうと、サンプリング終了後、会話をしてもノイズとして処理されて認識率が落ちてしまう。
      - 会話をしていけない時間は「会話モードを起動しました」の声が聞こえてから6秒間
        - マイクのサンプリングはデフォルトの  8,000 Hz なため、48,000 / 8,000 = 6(秒)

## 辞書の更新

  - 下記の手順に従ってjuliusの会話認識用の辞書を更新する

```
1. 辞書の元となるデータを作成して保存

ファイル名: hug_entity_sjis.csv
csv内容: 単語,よみがな
例: 今何時,いまなんじ
※単語は認識結果としてjuliusから返る文字列
※よみがなは音声の認識に利用される

2. sjisをutf8に変換
$ cd ~/hug/dic
$ iconv -f sjis -t utf8 hug_entity_sjis.csv > hug_entity.csv

3. TSVに変換
$ cat hug_entity.csv | tr "," "\\t" > hug_entity.tsv

4. EUC-JPに変換
$ iconv -f utf8 -t euc-jp hug_entity.tsv > hug_entity_eucjp.tsv

5. jujius dic型に変換
$ /home/pi/julius-kits/src/julius-4.4.2/gramtools/yomi2voca/yomi2voca.pl hug_entity_eucjp.tsv > hug_entity.dic
```
