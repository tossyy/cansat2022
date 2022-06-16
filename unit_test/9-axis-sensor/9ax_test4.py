#キャリブレーション後のテスト
from smbus import SMBus
import time
import math
import csv

MAG_ADDR = 0x13
MAG_R_ADDR = 0x42

i2c = SMBus(1)

def bmx_setup():

    # mag_data_setup : 地磁気値をセットアップ
    data = i2c.read_byte_data(MAG_ADDR, 0x4B)
    if(data == 0):
        i2c.write_byte_data(MAG_ADDR, 0x4B, 0x83)
        time.sleep(0.5)
    i2c.write_byte_data(MAG_ADDR, 0x4B, 0x01)
    i2c.write_byte_data(MAG_ADDR, 0x4C, 0x00)
    i2c.write_byte_data(MAG_ADDR, 0x4E, 0x84)
    i2c.write_byte_data(MAG_ADDR, 0x51, 0x04)
    i2c.write_byte_data(MAG_ADDR, 0x52, 0x16)
    time.sleep(0.5)


def mag_value():
    data = [0, 0, 0, 0, 0, 0, 0, 0]
    mag_data = [0.0, 0.0, 0.0]

    try:
        for i in range(8):
            data[i] = i2c.read_byte_data(MAG_ADDR, MAG_R_ADDR + i)

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

    return mag_data



if __name__ == "__main__":

    bmx_setup()
    time.sleep(0.1)

    try:
        x_max = -999999
        x_min = 999999
        y_max = -999999
        y_min = 99999
        x = []
        y = []

        while True:
            mag = mag_value()
            print("Mag -> x:{}, y:{}, z: {}".format(mag[0]+49.5, mag[1]-204, mag[2]))
            print("\n")
            if x_max < mag[0] :
                x_max = mag[0]
            if x_min > mag[0] :
                x_min = mag[0]
            if y_max < mag[1] :
                y_max = mag[1]
            if y_min > mag[1] :
                y_min = mag[1]
            x.append(mag[0])
            y.append(mag[1])

            time.sleep(0.2)

    except KeyboardInterrupt:
        print(x_max, x_min, y_max, y_min)
        print((x_max+x_min)/2, (y_max+y_min)/2)
        print(x)
        print(y)