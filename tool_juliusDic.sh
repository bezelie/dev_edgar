fs.writeFile(file_chatEntity, text , 'utf8', function (err) {
var COMMAND = 'sudo sed -E "s/,/    /g" '+file_chatEntity+' > '+file_chatEntity_tsv; // csvをtsvに変換
exec(COMMAND, function(error, stdout, stderr) { // tsvファイルをjuliusのdic形式に変換
var COMMAND = 'iconv -f utf8 -t eucjp '+file_chatEntity_tsv+' | /home/pi/dictation-kit-v4.4/src/julius-4.4.2/gramtools/yomi2voca/yomi2voca.pl > '+file_chatEntity_dic; // tsvをdicに変換
// var COMMAND = 'iconv -f utf8 -t eucjp chatEntity.tsv | /home/pi/dictation-kit-v4.4/src/julius-4.4.2/gramtools/yomi2voca/yomi2voca.pl > chatEntity.dic'; // tsvをdicに変換

subprocess.call(["sudo sh -c 'iconv -f utf8 -t eucjp julius.yomi | /home/pi/dictation-kit-v4.4/src/julius-4.4.2/gramtools/yomi2voca/yomi2voca.pl > julius.dic'"], shell=True)

