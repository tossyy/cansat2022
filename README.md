# <span style="color : #7cfc00"> cansat2022 </span>

## RaspberryPiの基本設定

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

## 使うかもしれないコマンド

* パスワードの変更　　`sudo passwd <user name>`  
新しいパスワードを聞かれるので次回以降使いたいパスワードを入力。  
* アップデート　　`sudo apt-get update`  
* アップグレード　　`sudo apt-get upgrade`  
* 再起動　　`sudo shutdown -r now`  
* シャットダウン　　`sudo shutdown -h now`  

## 開発の進め方

基本はpythonで書きます。ラズパイではcodeが使えないのでやりにくいと思います。PCの方でファイルを作って、scpで送信しましょう。  
```bash
scp <送信したいファイルのパス> pi@raspberrypi.local:<送信したい場所のパス>
```

## プログラムの実行方法

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
4. ゴール地点のGPSの値を取得します。
	```bash
	cd utat/cansat2022/main
	python remember_gps.py
	```
	位置情報は`utat/target_posision.txt`として保存されます。
5. 実行します。
	* **方法１**  
		sshでラズパイに接続し、以下を実行。ログはコンソールに出力される。
		```bash
		cd utat/cansat2022/main
		python main.py
		```
	* **方法２**  
	sshでラズパイに接続し、以下を実行。ログは`utat/log`に残る。
		```bash
		sudo systemctl start cansat
		```	
	* **方法3**  
	起動時に自動的に実行するようにする。ログは`utat/log`に残る。
		```bash
		# 自動実行有効化
		sudo systemctl enable cansat
		```
		```bash
		# 自動実行無効化
		sudo systemctl disable cansat
		```

## 起動時自動実行の設定方法

> [Raspberry Piでプログラムを自動起動する5種類の方法](https://qiita.com/karaage0703/items/ed18f318a1775b28eab4)

1. sshでラズパイに接続
2. 設定ファイルを作成。
	```bash
	sudo nano /etc/systemd/system/cansat.service
	```  
	`cansat.service`の中身は以下。
	```
	[Unit]
	Description = cansat daemon
	
	[Service]
	Type = simple
	Restart = no
	WorkingDirectory = /home/pi/utat/cansat2022/main
	ExecStart = /usr/bin/python /home/pi/utat/cansat2022/main/main.py
	StandardOutput = file:/home/pi/utat/log/log.txt
	StandardError = file:/home/pi/utat/log/error.txt
	
	[Install]
	WantedBy = multi-user.target
	```
3. 設定ファイルをロード
	```bash
	sudo systemctl load-daemon
	```  
デーモンの状態は、
```bash
sudo systemctl status cansat
```
で確認できる。