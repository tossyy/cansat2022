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


    def calibrate(self, motor):
        print("caliblation start")
        x_list = []
        y_list = []
        gx_list = []
        gy_list = []
        interval = 0.3
        around_time = 3
        N = int(around_time/interval)
        start_time = time.perf_counter()

        #15秒間，値を取る
        motor.change_speed(50)
        motor.func_right()
        while time.perf_counter() - start_time < 15:
            mag_value = self.get_mag_value()
            x_list.append(mag_value[0])
            y_list.append(mag_value[1])
            
            time.sleep(interval)
        
        motor.func_brake()
        
        for i in range(len(x_list)-N):
            gx_list.append(sum(x_list[i:i+N])/ N)
            gy_list.append(sum(y_list[i:i+N])/ N)
        
        self.correction_x = sum(gx_list) / len(gx_list)
        self.correction_y = sum(gy_list) / len(gy_list)

        x_list_corrected = [v - self.correction_x for v in x_list]
        y_list_corrected = [v - self.correction_y for v in y_list]

        path_raw = '../../mag_value_raw.csv'
        path_corrected = '../../mag_value_corrected.csv'

        with open(path_raw, mode='w') as f:
            writer = csv.writer(f)
            for x,y in zip(x_list, y_list):
                writer.writerow([x, y])
        
        with open(path_corrected, mode='w') as f:
            writer = csv.writer(f)
            for x,y in zip(x_list_corrected, y_list_corrected):
                writer.writerow([x, y])

        print("caliblation finish")




