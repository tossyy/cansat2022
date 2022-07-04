class Pressure: #気圧センサ

    ADDRESS = 0x5C 
    CTRL_REG1 = 0x20
    PRESS_OUT_XL = 0x28 #最下位8ビット
    PRESS_OUT_L = 0x29 #下位8ビット
    PRESS_OUT_H = 0x2A #上位8ビット
    LPS25H_WHO_ID = 0xBD #今回使う気圧センサのアドレス

    def __init__(self, i2c):
        self.i2c = i2c
        self.i2c.write_byte_data(self.ADDRESS, self.CTRL_REG1, 0x90)
        print("気圧センサ初期化完了")

    
    def get_pressure(self): #2進数のまま気圧のデータを返す
        p = self.i2c.read_i2c_block_data(self.ADDRESS,self.PRESS_OUT_XL,1)
        p += self.i2c.read_i2c_block_data(self.ADDRESS,self.PRESS_OUT_L,1)
        p += self.i2c.read_i2c_block_data(self.ADDRESS,self.PRESS_OUT_H,1)
        return (p[2] << 16 | p[1] << 8 | p[0]) / 4096 #データの接合