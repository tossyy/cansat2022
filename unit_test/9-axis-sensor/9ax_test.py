#!/usr/bin/python3
# -*- coding: utf-8 -*-

import smbus
import time

ACC_ADDRESS = 0x19
ACC_REGISTER_ADDRESS = 0x02
GYRO_ADDR = 0x69

i2c = smbus.SMBus(1)

i2c.write_byte_data(GYRO_ADDR, 0x0F, 0x04)
# Select Bandwidth register, 0x10(16)
#       0x07(07)    ODR = 100 Hz
i2c.write_byte_data(GYRO_ADDR, 0x10, 0x07)
# Select LPM1 register, 0x11(17)
#       0x00(00)    Normal mode, Sleep duration = 2ms
i2c.write_byte_data(GYRO_ADDR, 0x11, 0x00)

def bmx055():
    # initialize

    ## 指定したレジスタアドレスから、2byte分取得する
    x_lsb = i2c.read_byte_data(ACC_ADDRESS, ACC_REGISTER_ADDRESS)
    x_msb = i2c.read_byte_data(ACC_ADDRESS, ACC_REGISTER_ADDRESS+1)
    y_lsb = i2c.read_byte_data(ACC_ADDRESS, ACC_REGISTER_ADDRESS+2)
    y_msb = i2c.read_byte_data(ACC_ADDRESS, ACC_REGISTER_ADDRESS+3)
    z_lsb = i2c.read_byte_data(ACC_ADDRESS, ACC_REGISTER_ADDRESS+4)
    z_msb = i2c.read_byte_data(ACC_ADDRESS, ACC_REGISTER_ADDRESS+5)

    x_value = (x_msb * 16) + ((x_lsb & 0xF0) / 16)
    x_value = x_value if x_value < 2048 else x_value - 4096
    y_value = (y_msb * 16) + ((y_lsb & 0xF0) / 16)
    y_value = y_value if y_value < 2048 else y_value - 4096
    z_value = (z_msb * 16) + ((z_lsb & 0xF0) / 16)
    z_value = z_value if z_value < 2048 else z_value - 4096

    x_acc = x_value * 0.00098*9.8
    y_acc = y_value * 0.00098*9.8
    z_acc = z_value * 0.00098*9.8

    print ("[%f, %f, %f]" % (x_acc, y_acc, z_acc))

    i2c.close()

def gyro():
    xG = yG = zG = 0

    try:
        data = i2c.read_i2c_block_data(GYRO_ADDR, 0x02, 6)
        # Convert the data
        xG = (data[1] * 256) + data[0]
        if xG > 32767:
            xG -= 65536

        yG = (data[3] * 256) + data[2]
        if yG > 32767:
            yG -= 65536

        zG = (data[5] * 256) + data[4]
        if zG > 32767:
            zG -= 65536

    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))

    print([xG, yG, zG])


if __name__ == '__main__':
    while True:
        gyro()
        time.sleep(0.5)
