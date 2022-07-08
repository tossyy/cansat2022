import smbus
from time import sleep

#オブジェクト生成
i2c = smbus.SMBus(1)

#アドレス定義
address = 0x5C
CTRL_REG1 = 0x20
PRESS_OUT_XL = 0x28 #最下位ビット
PRESS_OUT_L = 0x29 #下位ビット
PRESS_OUT_H = 0x2A #上位ビット

#Lセンサーの設定
i2c.write_byte_data(address, CTRL_REG1, 0x90)

while True:
    #データの読み込み
    pxl = i2c.read_byte_data(address, PRESS_OUT_XL)
    pl = i2c.read_byte_data(address, PRESS_OUT_L)
    ph = i2c.read_byte_data(address, PRESS_OUT_H)
    
    #データの統合
    prs = ph << 16 | pl << 8 | pxl
    #データの変換
    prs = prs / 4096
    print(round(prs, 2))
    sleep(1)


