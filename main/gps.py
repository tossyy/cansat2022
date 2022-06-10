import pigpio as pig #ピンの設定に使います
import smbus #気圧センサの管理に使います
from time import sleep #時間間隔に使います

class Gps: #GPS

    gps_out = 11 #GPS（出力）
    gps_in = 12 #GPS（読取）

    def __init__(self, pi):
        self.pi = pi
        self.pi.set_mode(gps_out, pig.OUTPUT)
        self.pi.set_mode(gps_in, pig.INPUT)