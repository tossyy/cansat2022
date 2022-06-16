# <span style="color : #7cfc00"> cansat2022 </span>

## <span style="color : #00ffff"> RaspberryPiの基本設定 </span>

1. Raspbianを公式サイトからインストール
2. SDカードフォーマッタをダウンロード
3. SDカードとPCを繋げてSDカードフォーマッタでフォーマット
4. Raspbian をSDカードに流し込む。GUI使わないなら、Liteで大丈夫っぽい。ここでパスワードなども設定する
5. SDカードにSSHとWi-fiの設定を書き込む。
	1. ターミナル開く（以下ここに入力）
	2. `cd /Volumes/boot`（SDカードに入る）
	3. `touch ssh`（sshという空のファイルを作る。これでsshが有効になってターミナルからログイン可能。）
	4. wpa_supplicant.conf を作成（`code wpa_supplicant.conf`とかで良い）
	5. wpa_supplicant.confの中身を以下のように編集

		(1)家のwi-fiとかを使う場合  
		```bash
		ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
		update_config=1
		country=JP
		
		network={
		ssid="接続したいWi-FiのSSID"
		psk="パスワード"
		key_mgmt=WPA-PSK
		}
		```   

		(2)テザリングする場合  
		```bash
		ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
		update_config=1
		country=JP

		network={
			ssid="SSID(=スマホの名前)"
			psk="パスワード"
			proto=RSN
			priority=1
			id_str="mobile"
		}
		```
6. Raspberry pi zero とPCを有線で繋ぐ。（電源供給用）
7. ターミナルを開いて、`ssh pi@raspberrypi.local` を打ち込む。（raspberrypiのところはたぶんホスト名？OSをSDカードに焼くときに設定から決められるはず）
8. 質問にyesと答える。
9. パスワードを入力（今回はcansat。デフォだとraspberry。これもOSをSDカードに焼く時の設定から決められる）

## <span style="color : #00ffff"> 使うかもしれないコマンド </span>

* パスワードの変更　　`sudo passwd <user name>`  
新しいパスワードを聞かれるので次回以降使いたいパスワードを入力。  
* アップデート　　`sudo apt-get update`  
* アップグレード　　`sudo apt-get upgrade`  
* 再起動　　`sudo shutdown -r now`  
* シャットダウン　　`sudo shutdown -h now`  

## <span style="color : #00ffff"> 開発の進め方 </span>

基本はpythonで書きます。ラズパイではcodeが使えないのでやりにくいと思います。PCの方でファイルを作って、scpで送信しましょう。  
```bash
scp <送信したいファイルのパス> pi@raspberrypi.local:<送信したい場所のパス>
```

## <span style="color : #00ffff"> プログラムの実行方法 </span>

1. RaspberryPiの環境を整えてください。以下のドキュメントを参照してください。
	* [I2Cのドキュメント](https://github.com/tossyy/cansat2022/blob/master/unit_test/i2c/I2C.md)
	* [GPSのドキュメント](https://github.com/tossyy/cansat2022/blob/master/unit_test/gps/gps_doc.md)
2. [このスケッチ](https://github.com/tossyy/cansat2022/blob/master/unit_test/arduino/i2c_test.cpp)をArduinoに書き込んでください。
3. RaspberryPiは以下のようなディレクトリ構造にしてください
```
~/
└── utat
	├── cansat2022
	└── log
```
4. `cansat2022/main/main.py`を実行します。
	* 方法１【RaspberryPiの起動と同時にファイルが実行されるようにする】
		`/etc/rc.local`に
		```bash
		python ~/utat/cansat2022/main/main.py 1> ~/utat/log/log.txt 2> ~/utat/log/error.txt
		```
		と書き込む。
		> [Raspberry Piでプログラムを自動起動する5種類の方法](https://qiita.com/karaage0703/items/ed18f318a1775b28eab4)
	* 方法２【RaspberryPiにパソコンからSSH接続して実行】