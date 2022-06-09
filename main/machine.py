import pigpio as pig #ピンの設定に使います
import smbus #気圧センサの管理に使います
from time import sleep #時間間隔に使います

#ピン番号を設定
#数字は仮置きです
motor_r1 = 1 #モーターR（前進）
motor_l1 = 2 #モーターL（前進）
motor_r2 = 3 #モーターR（後退）
motor_l2 = 4 #モーターL（後退）
sensa_9_out = 5 #9軸センサ（出力）
sensa_9_in = 6 #9軸センサ（読取）
sensa_baro_out = 7 #気圧センサ（出力）
sensa_baro_in = 8 #気圧センサ（読取）
sensa_light_out = 9 #光センサ（出力）
sensa_light_in = 10 #光センサ（読取）
gps_out = 11 #GPS（出力）
gps_in = 12 #GPS（読取）



class Motor: #モーター

    def __init__(self, pi):
        self.pi = pi
        self.pi.set_mode(motor_r1, pig.OUTPUT) #各ピンを出力に設定
        self.pi.set_mode(motor_l1, pig.OUTPUT)
        self.pi.set_mode(motor_r2, pig.OUTPUT)
        self.pi.set_mode(motor_l2, pig.OUTPUT)

    def motor_r_forward(self): #前進（R）
        self.pi.write(motor_r1, 1)
        self.pi.wtite(motor_r2, 0)
    
    def motor_l_forward(self): #前進（L）
        self.pi.write(motor_l1, 1)
        self.pi.wtite(motor_l2, 0)

    def motor_r_backward(self): #後退（R）
        self.pi.write(motor_r1, 0)
        self.pi.wtite(motor_r2, 1)

    def motor_l_backward(self): #後退（L）
        self.pi.write(motor_l1, 0)
        self.pi.wtite(motor_l2, 1)

    def motor_r_stop(self): #停止（R）
        self.pi.write(motor_r1, 0)
        self.pi.wtite(motor_r2, 0)

    def motor_l_stop(self): #停止（L）
        self.pi.write(motor_l1, 0)
        self.pi.wtite(motor_l2, 0)

    def motor_forward(self): #前進（R＋L）
        self.motor_r_forward()
        self.motor_l_forward()
    
    def motor_backward(self): #後退（R+L）
        self.motor_r_backward()
        self.motor_l_backward()
    
    def motor_stop(self): #停止（R＋L）
        self.motor_r_stop()
        self.motor_l_stop()

class Sensa_9: #9軸センサ

    def __init__(self, pi):
        self.pi = pi
        self.pi.set_mode(sensa_9_out, pig.OUTPUT)
        self.pi.set_mode(sensa_9_in, pig.INOUT)

class Sensa_baro: #気圧センサ

    i2c = smbus.SMBus(1) #オブジェクト生成
    address = 0x5C 
    CTRL_REG1 = 0x20
    PRESS_OUT_XL = 0x28 #最下位8ビット
    PRESS_OUT_L = 0x29 #下位8ビット
    PRESS_OUT_H = 0x2A #上位8ビット
    WHO_AM_I = 0x0F #who_am_i用のアドレス
    LPS25H_WHO_ID = 0xBD #今回使う気圧センサのアドレス

    def __init__(self, pi):
        self.pi = pi
        self.pi.set_mode(sensa_baro_out, pig.OUTPUT)
        self.pi.set_mode(sensa_baro_in, pig.INPUT)
        self.i2c.write_byte_data(self.address, self.CTRL_REG1, 0x90) #
    
    def testWhoAmI(self):
        return self.i2c.read_i2c_block_data(self.address, self.WHO_AM_I, 1)
    
    def detectDvice(self): #接続デバイスがLPS25HBか確認。okならTrue
        self.id = self.testWhoAmI()
        if (self.id[0] == self.LPS25H_WHO_ID) :
            return True
        return False
    
    def readPressureRaw(self): #2進数のまま気圧のデータを返す
        p = self.i2c.read_i2c_block_data(self.address,self.PRESS_OUT_XL,1)
        p += self.i2c.read_i2c_block_data(self.address,self.PRESS_OUT_L,1)
        p += self.i2c.read_i2c_block_data(self.address,self.PRESS_OUT_H,1)
        return p[2] << 16 | p[1] << 8 | p[0] #データの接合
    
    def readPressurehPa(self):
        return self.readpressureRaw() / 4096

class Sensa_light: #光センサ

    def __init__(self, pi):
        self.pi = pi
        self.pi.set_mode(sensa_light_out, pig.OUTPUT)
        self.pi.set_mode(sensa_light_in, pig.INPUT)


class Gps: #GPS

    def __init__(self, pi):
        self.pi = pi
        self.pi.set_mode(gps_out, pig.OUTPUT)
        self.pi.set_mode(gps_in, pig.INPUT)


class Machine: #機体

    def __init__(self): #全ての機能を搭載
        self.pi = pig.pi()
        self.motor = Motor(self.pi)
        self.sensa_9 = Sensa_9(self.pi)
        self.sensa_baro = Sensa_baro(self.pi)
        self.sensa_light = Sensa_light(self.pi)
        self.gps = Gps(self.pi)


    def phase1(self): #phase1。放出判定。
        print("phase1 hajime")
        while True :
            if self.sensa_baro.detectDvice() != False:
                continue
            break

        print("phase1 owari")

    def phase2(self):
        print("phase2 hajime")
        print("phase2 owari")
    
    def phase3(self):
        print("phase3 hajime")
        print("phase3 owari")

    def run(self):
        self.phase1()
        self.phase2()
        self.phase3()
