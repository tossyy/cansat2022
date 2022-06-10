import pigpio as pig #ピンの設定に使います
import smbus #気圧センサの管理に使います
from time import sleep #時間間隔に使います

class Sensa_9: #9軸センサ

    sensa_9_out = 5 #9軸センサ（出力）
    sensa_9_in = 6 #9軸センサ（読取）

    def __init__(self, pi):

        self.pi = pi
        self.pi.set_mode(self.sensa_9_out, pig.OUTPUT)
        self.pi.set_mode(self.sensa_9_in, pig.INOUT)