# cansat2022

ラズパイを使えるようにするまで

Raspbian を公式サイトからインストール
↓
SDカードフォーマッタをダウンロード
↓
SDカードとPCを繋げてSDカードフォーマッタでフォーマット
↓
Raspbian をSDカードに流し込む。GUI使わないなら、LIteで大丈夫っぽい。
↓
Home-brewを使ったvimの再インストール。これしないと多分vimが使えない？多分いらない。
（参考サイト：https://original-game.com/vim-mac/ ）
↓
SDカードにSSHとWi-fiの設定を書き込む。GUI環境じゃないならこれやらないと多分何もできない。
1. ターミナル開く（以下ここに入力）
2. cd /Volumes/boot（SDカードに入る）
3. touch ssh（sshというか空のファイルを作る。これでsshが有効になってターミナルからログイン可能。）
4. vim wpa_supplicant.conf（vimを用いてwpa_supplicant.confというファイルを、SDカードのルートディレクトリに作成）

wpa_supplicant.confの中身は以下のように編集。vimの使い方はこちら（→https://qiita.com/okamos/items/c97970ab34ff55ff3167 特に「挿入モード」、「保存」、「終了」に気を付ける）。

1. ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
2. update_config=1
3. country=JP
4.  
5. network={
6.  ssid="接続したいWi-FiのSSID"
7.  psk="パスワード"
8.  key_mgmt=WPA-PSK
9. }
10. 
（参考サイト：https://www.penpale.jp/blog/raspberry_pi_zero_w_setup_without_monitor.html 、 https://robopara.co.jp/%E3%83%87%E3%82%A3%E3%82%B9%E3%83%97%E3%83%AC%E3%82%A4%E3%82%92%E4%BD%BF%E3%82%8F%E3%81%9A%E3%81%ABraspberry-pi-zero-w-%E3%81%ABraspbian-lite%E3%82%92%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC/ ）

 ↓
Raspberry pi zero とPCを有線で繋ぐ。
↓
ターミナルを開いて、ssh pi@raspberrypi.local を打ち込む。（raspberrypiのところはたぶんホスト名？OSをSDカードに焼くときに設定から決められるはず）
↓
謎の質問にyesと答える。
↓
パスワードを入力（今回はcansat。デフォだとraspberry。これもOSをSDカードに焼く時の設定から決められる）


オプション的要素

・パスワードの変更　　sudo passwd <user name>　新しいパスワードを聞かれるので次回以降使いたいパスワードを入力。
・アップデート　　sudo apt-get update
・アップグレード　　sudo apt-get upgrade
・再起動　　sudo shutdown -r now
・シャットダウン　　sudo shutdown -h now

実行にあたって

Wiring Pi とは、ラズパイでGPIOを制御するのに必要なC言語用のライブラリのこと。WiringPiをインストールするとgpioというコマンドもインストールされる。このコマンドを使うと、シェル上でGPIOを制御することができる。
・まずはCで動かすので、WiringPiを入れる。pi@raspberry下で
	1.  sudo apt-get install libi2c-dev
	2.  sudo apt-get install git-core　 （gitのインストール）
	3.  cd ~ （ホームディレクトリへ移動）
	4.  git clone https://github.com/WiringPi/WiringPi.git （Wiring Pi のソースコードが wiringPiディレクトリとしてクローン）
	5.  cd WiringPi（WiringPiディレクトリへ移動）
	6.  ./build（ビルドする）

実行ファイルの作り方

・基本はC++を使ってVScodeとかの書きやすいエディタを使ってコード書いて、vi（viで起動）に編集モード（i）下でコピペ。その後escでノーマルモードに戻って、:w ファイル名 で保存が良いと思う。拡張子は.cppで。
・コード保存用のファイルがあった方が良いのかな？cppというファイルを作りました。（というかSDカードに直接書けば良いのかもしれない。）
・作ったファイルはコンパイルする。
・コンパイルはターミナルで　g++ -o <指定実行ファイル名> <コンパイルするファイル名> を用いる。（コンパイルすると実行ファイル〇〇.exe（.outかも）というファイルが作られるらしい。多分何も指定しないとa.exeみたいなが作られるぽい。整理のためにもコンパイルファイル名と同じにしといたほうが賢明な気がする。(ex) g++ test test.cpp）
・多分上だけじゃダメで、ライブラリパス（とインクルードパス？←いるかわかんない）が必要になる。g++ -o test test.cpp -I/usr/local/include -L/usr/local/lib -lwiringPi こんな感じので動いたからこれでコピペしていいかもしれない。
・g++ -Wall -o blink blink.cpp  とかでも多分いけそう。
・実行は、./ファイル名（(ex) ./test）　できなかったら、sudo ./ファイル名　でやってみる
・やめ方：control + z で止まる（Macで）

補足
・https://monomonotech.jp/kurage/raspberrypi/linux_command.html　コマンド集。これからお世話になるはず。
・外でラズパイ使うならスマホでテザリングする（SDカードの書き込みを変更しよう）。
・https://qazsedcftf.blogspot.com/2020/12/raspberry-pi-c-led-pwm.html

