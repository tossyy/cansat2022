import pigpio as pig #ピンの設定に使います
import smbus #気圧センサの管理に使います
from time import sleep #時間間隔に使います

#ピン番号を設定
#数字は仮置きです






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
