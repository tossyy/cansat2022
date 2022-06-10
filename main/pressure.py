import pigpio as pig #ピンの設定に使います
import smbus #気圧センサの管理に使います
from time import sleep #時間間隔に使います

class Pressure: #気圧センサ

    ADDRESS = 0x5C 
    CTRL_REG1 = 0x20
    PRESS_OUT_XL = 0x28 #最下位8ビット
    PRESS_OUT_L = 0x29 #下位8ビット
    PRESS_OUT_H = 0x2A #上位8ビット
    WHO_AM_I = 0x0F #who_am_i用のアドレス
    LPS25H_WHO_ID = 0xBD #今回使う気圧センサのアドレス

    def __init__(self, pi, i2c):
        self.i2c = i2c
        self.pi = pi
        self.pi.set_mode(self.sensa_baro_out, pig.OUTPUT)
        self.pi.set_mode(self.sensa_baro_in, pig.INPUT)
        self.i2c.write_byte_data(self.ADDRESS, self.CTRL_REG1, 0x90) 
    
    def test_who_am_I(self, i2c):
        return self.i2c.read_i2c_block_data(self.ADDRESS, self.WHO_AM_I, 1)
    
    def detect_dvice(self, i2c): #接続デバイスがLPS25HBか確認。okならTrue
        self.id = self.test_who_am_I()
        if (self.id[0] == self.LPS25H_WHO_ID) :
            return True
        return False
    
    def get_pressure_raw(self, i2c): #2進数のまま気圧のデータを返す
        p = self.i2c.read_i2c_block_data(self.ADDRESS,self.PRESS_OUT_XL,1)
        p += self.i2c.read_i2c_block_data(self.ADDRESS,self.PRESS_OUT_L,1)
        p += self.i2c.read_i2c_block_data(self.ADDRESS,self.PRESS_OUT_H,1)
        return p[2] << 16 | p[1] << 8 | p[0] #データの接合
    
    def read_pressure_hPa(self, i2c):
        return self.get_pressure_raw() / 4096