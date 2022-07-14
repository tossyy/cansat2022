import time #時間間隔に使います
import csv

class Nine: #9軸センサ

    MAG_ADDR = 0x13
    MAG_R_ADDR = 0x42
    correction_x = 0
    correction_y = 0

    def __init__(self, i2c):
        self.i2c = i2c #smbus
        self.bmx_setup()

        print("9軸センサ初期化完了")
    
    def bmx_setup(self):

    # mag_data_setup : 地磁気値をセットアップ
        data = self.i2c.read_byte_data(self.MAG_ADDR, 0x4B)
        if(data == 0):
            self.i2c.write_byte_data(self.MAG_ADDR, 0x4B, 0x83)
            time.sleep(0.3)
        self.i2c.write_byte_data(self.MAG_ADDR, 0x4B, 0x01)
        self.i2c.write_byte_data(self.MAG_ADDR, 0x4C, 0x00)
        self.i2c.write_byte_data(self.MAG_ADDR, 0x4E, 0x84)
        self.i2c.write_byte_data(self.MAG_ADDR, 0x51, 0x04)
        self.i2c.write_byte_data(self.MAG_ADDR, 0x52, 0x16)
        time.sleep(0.3)
    
    def get_mag_value(self):
        data = [0, 0, 0, 0, 0, 0, 0, 0]
        mag_value = [0.0, 0.0, 0.0]

        try:
            for i in range(8):
                data[i] = self.i2c.read_byte_data(self.MAG_ADDR, self.MAG_R_ADDR + i)

            for i in range(3):
                if i != 2:
                    mag_value[i] = ((data[2*i + 1] * 256) + (data[2*i] & 0xF8)) / 8
                    if mag_value[i] > 4095:
                        mag_value[i] -= 8192
                else:
                    mag_value[i] = ((data[2*i + 1] * 256) + (data[2*i] & 0xFE)) / 2
                    if mag_value[i] > 16383:
                        mag_value[i] -= 32768

        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))

        return mag_value
    
    def get_mag_value_corrected(self):
        mag_value = self.get_mag_value()
        mag_value_corrected = [mag_value[0]-self.correction_x, mag_value[1]-self.correction_y, mag_value[2]]

        return mag_value_corrected




