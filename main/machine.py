import pigpio as pig #ピンの設定に使います
import smbus #気圧センサの管理に使います
from time import sleep #時間間隔に使います
from motor import Motor
from nine import Nine
from pressure import Pressure
from gps import Gps
from light import Light
from jump import Jump

class Machine: #機体

    def __init__(self): #全ての機能を搭載
        self.i2c = smbus.SMBus
        self.pi = pig.pi()
        self.motor = Motor(self.pi)
        self.nine = Nine(self.pi, self.i2c)
        self.pressure = Pressure(self.pi, self.i2c)
        self.light = Light(self.pi, self.i2c)
        self.gps = Gps(self.pi)
        


    def phase1(self): #phase1。放出判定。
        print("phase1 hajime")
        while True :
            if self.sensa_baro.detectDvice() != False:
                continue
            break

        while True :



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
