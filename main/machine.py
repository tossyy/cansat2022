import pigpio as pig #ピンの設定に使います
import smbus #気圧センサの管理に使います
from time import sleep, perf_counter, time #時間間隔に使います
from motor import Motor
from nine import Nine
from pressure import Pressure
from gps import GPS
from light import Light
from jump import Jump
from statistics import median, stdev

class Machine: #機体

    def __init__(self): #全ての機能を搭載
        self.i2c = smbus.SMBus(1)
        self.pi = pig.pi()
        self.motor = Motor(self.pi)
        self.nine = Nine(self.pi, self.i2c)
        self.pressure = Pressure(self.pi, self.i2c)
        self.light = Light(self.pi, self.i2c)
        self.gps = GPS(self.pi, self.i2c)
        self.jump = Jump(self.pi, self.i2c)
        


    def phase1(self): #phase1。放出判定。
        print("phase1 hajime")
        print("phase1 owari")

    def phase2(self): #phase2。着地判定。
        print("phase2 hajime")
        pres_judge = False
        gps_judge = False
        time_judge = False
        time_start = perf_counter()
        time_end = perf_counter()

        while True :
            if pres_judge and gps_judge: #GPSと気圧センサによる着地判定
                print("GPS & pressure")
                break

            if time_judge: #120秒経過による着地判定
                print("time")
                break

            if not pres_judge:
                p_list = []
                for i in range(4):
                    p_list.append(self.pressure.get_pressure_hPa())
                    sleep(5)
            
            if time_end-time_start < 120:
                time_end = perf_counter()
            else :
                time_judge = True



        print("phase2 owari")
    
    def phase3(self):
        print("phase3 hajime")
        print("phase3 owari")

    def run(self):
        self.phase1()
        self.phase2()
        self.phase3()
