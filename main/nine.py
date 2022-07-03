import smbus #気圧センサの管理に使います
import time #時間間隔に使います
from motor import Motor

class Nine: #9軸センサ

    MAG_ADDR = 0x13
    MAG_R_ADDR = 0x42
    correction_x = 0
    correction_y = 0

    def __init__(self, i2c):
        self.i2c = i2c #smbus
    
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
        mag_data = [0.0, 0.0, 0.0]

        try:
            for i in range(8):
                data[i] = self.i2c.read_byte_data(self.MAG_ADDR, self.MAG_R_ADDR + i)

            for i in range(3):
                if i != 2:
                    mag_data[i] = ((data[2*i + 1] * 256) + (data[2*i] & 0xF8)) / 8
                    if mag_data[i] > 4095:
                        mag_data[i] -= 8192
                else:
                    mag_data[i] = ((data[2*i + 1] * 256) + (data[2*i] & 0xFE)) / 2
                    if mag_data[i] > 16383:
                        mag_data[i] -= 32768

        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))

        mag = [mag_data[0]-self.correction_x, mag[1]-self.correction_y, mag[2]] #補正
        return mag

    def cul_centergravity(self, x, y):
        return [sum(x)/len(x), sum(y)/len(y)]
    
    def calibrate(self, motor):
        print("caliblation start")
        self.motor = motor
        x = []
        y = []
        g_x = []
        g_y = []
        start_time = time.perf_counter()

        #10秒間，値を取る
        motor.change_speed(20)
        motor.func_right()
        while time.perf_counter() - start_time < 10:
            mag = self.get_mag_value()
            x.append(mag[0])
            y.append(mag[1])

            #ある程度きたら，重心を撮り続ける
            if time.perf_counter() - start_time > 2:
                g_x.append(self.cul_centergravity()[0])
                g_y.append(self.cul_centergravity()[1])
            time.sleep(0.3)
        
        motor.func_brake()
        
        #g_yが一番大きくなるインデックスをとる。
        max_index = g_y.index(max(g_y)) 
        #一週
        #周くらいしたときに重心が一番上よりなものを補正とする
        self.correction_x = g_x[max_index]
        self.correction_y = g_y[max_index]

        print("caliblation finish")




