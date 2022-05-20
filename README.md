# <span style="color : #7cfc00"> cansat2022 </span>

## <span style="color : #00ffff"> RaspberryPiの基本設定 </span>

Raspbianを公式サイトからインストール  
↓  
SDカードフォーマッタをダウンロード  
↓  
SDカードとPCを繋げてSDカードフォーマッタでフォーマット  
↓  
Raspbian をSDカードに流し込む。GUI使わないなら、Liteで大丈夫っぽい。  
↓  
SDカードにSSHとWi-fiの設定を書き込む。GUI環境じゃないならこれやらないと多分何もできない。  
1. ターミナル開く（以下ここに入力）
2. cd /Volumes/boot（SDカードに入る）
3. touch ssh（sshというか空のファイルを作る。これでsshが有効になってターミナルからログイン可能。）  
4. wpa_supplicant.conf を作成（code wpa_supplicant.confとかで良い）  

↓  
wpa_supplicant.confの中身を以下のように編集

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
↓  
Raspberry pi zero とPCを有線で繋ぐ。  
↓  
ターミナルを開いて、ssh pi@raspberrypi.local を打ち込む。（raspberrypiのところはたぶんホスト名？OSをSDカードに焼くときに設定から決められるはず）  
↓  
質問にyesと答える。  
↓  
パスワードを入力（今回はcansat。デフォだとraspberry。これもOSをSDカードに焼く時の設定から決められる）  


## <span style="color : #00ffff"> 使うかもしれないコマンド </span>

* パスワードの変更　　`sudo passwd <user name>`  
新しいパスワードを聞かれるので次回以降使いたいパスワードを入力。  
* アップデート　　`sudo apt-get update`  
* アップグレード　　`sudo apt-get upgrade`  
* 再起動　　`sudo shutdown -r now`  
* シャットダウン　　`sudo shutdown -h now`  

## <span style="color : #00ffff"> 実行にあたって </span>

基本はpythonで実行します。  
ラズパイではcodeが使えないのでやりにくいと思います。PCの方でファイルを作って、scpで送信しましょう。  
`scp <送信したいファイルのパス> pi@raspberrypi.local:<送信したい場所のパス>`  
送信したい場所のパスは多分 ~/py とか。
