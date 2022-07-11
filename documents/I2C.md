# I2Cについてのドキュメント

間違ったこと書いてあったら訂正お願いします。  
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

## I2Cインターフェースについて

I2C機器には通信の親機（マスターノード、raspberrypiとか）と子機（スレーブノード、センサーとか）の2種類がある。I2C機器にはあらかじめアドレスが割り当てられており、マスターがスレーブを特定する際にアドレスを用いる。  
I2Cアドレスにはあらかじめ10進数で8~119までの番号が割り振られている。これが16真数だったり、2進数だったり、7bitや8bitになるのでややこしい。

## I2CToolsの使い方

[I2C Toolsの簡単な使い方について](https://moba1.hatenablog.com/entry/2019/10/09/114145)を参考にした。  
I2C-Toolsのうち, i2cdetect, i2cget, 多分良く使うので簡単な使い方を記しておく。  
### I2Cdetect
基本的な文法は, 
```bash
i2cdetect -V
i2cdetect -l
i2cdetect -F i2cbus
i2cdetect [-y] [-a] [-q|-r] i2cbus [first last]
```
このうち, `i2cdetect [-y] [-a] [-q|-r] i2cbus [first last]`がよく使うと思われるので, これの説明を書いておく。  
良く使うのは`-y`でこれは対話形式にしないようにするためのオプション。  
`i2cdetect -y 1`で反応のあった機器のアドレスがわかる。1はi2cbusである。

### I2Cget
基本は`i2cget [-f] [-y] i2cbus chip-address [data-address [mode]]`といった形で書く。`chip-address`にはi2cdetectで調べたときに反応があったスレーブアドレスを指定する。`data-address`は利用できるスレーブアドレス下にあるデバイスに対してRead/Writeを行いたいアドレスを指定する。  
例えば, `i2cget -y 1 0x4a 0x0f`みたいな感じ。`0x4a`は反応のあったスレーブアドレス。`0x0f`はWHO_AM_Iアドレスであり, ここの値を読みたい。
