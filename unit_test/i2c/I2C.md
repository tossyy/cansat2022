# I2Cについてのドキュメント

間違ったこと書いてあったら訂正いお願いします。  
参考サイト:[ラズパイで初めてのI2C通信のやり方](https://101010.fun/iot/adc-i2c-raspberry-pi-zero.html)

## RaspberryPiでI2Cを使えるように設定

`i2c-tools`ライブラリをインストールする。
```bash
sudo apt-get update
sudo apt-get install i2c-tools
```
インストールが終わったら、`sudo raspi-config`でI2Cを有効にする。  
> 設定画面の`5.Interacing Option`に進み、`P5 I2C`へ進み、`Enable` にする。

## PythonでI2Cを使えるように設定

PythonプログラムでもI2C通信を使いたい場合、`python-smbus`ライブラリをインストールする。これはpython2と3で別れてるらしい。どっちも入れといた方がいいのかもしれない。
```bash
sudo apt-get install python-smbus
sudo apt-get install python3-smbus
```
（今回はこの方法で行わなかったような気がする、、、）

# I2Cインターフェースについて

I2C機器には通信の親機（マスターノード、raspberrypiとか）と子機（スレーブノード、センサーとか）の2種類がある。I2C機器にはあらかじめアドレスが割り当てられており、マスターがスレーブを特定する際にアドレスを用いる。  
I2Cアドレスにはあらかじめ10進数で8~119までの番号が割り振られている。これが16真数だったり、2進数だったり、7bitや8bitになるのでややこしい。