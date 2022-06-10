import pigpio as pig #ピンの設定に使います
import smbus #気圧センサの管理に使います
from time import sleep #時間間隔に使います


class Motor: #モーター
    motor_r1 = 1 #モーターR（前進）
    motor_l1 = 2 #モーターL（前進）
    motor_r2 = 3 #モーターR（後退）
    motor_l2 = 4 #モーターL（後退）

    def __init__(self, pi):
        self.pi = pi
        self.pi.set_mode(self.motor_r1, pig.OUTPUT) #各ピンを出力に設定
        self.pi.set_mode(self.motor_l1, pig.OUTPUT)
        self.pi.set_mode(self.motor_r2, pig.OUTPUT)
        self.pi.set_mode(self.motor_l2, pig.OUTPUT)

    def motor_r_forward(self): #前進（R）
        self.pi.write(self.motor_r1, 1)
        self.pi.wtite(self.motor_r2, 0)
    
    def motor_l_forward(self): #前進（L）
        self.pi.write(self.motor_l1, 1)
        self.pi.wtite(self.motor_l2, 0)

    def motor_r_backward(self): #後退（R）
        self.pi.write(self.motor_r1, 0)
        self.pi.wtite(self.motor_r2, 1)

    def motor_l_backward(self): #後退（L）
        self.pi.write(self.motor_l1, 0)
        self.pi.wtite(self.motor_l2, 1)

    def motor_r_stop(self): #停止（R）
        self.pi.write(self.motor_r1, 0)
        self.pi.wtite(self.motor_r2, 0)

    def motor_l_stop(self): #停止（L）
        self.pi.write(self.motor_l1, 0)
        self.pi.wtite(self.motor_l2, 0)

    def motor_forward(self): #前進（R＋L）
        self.motor_r_forward()
        self.motor_l_forward()
    
    def motor_backward(self): #後退（R+L）
        self.motor_r_backward()
        self.motor_l_backward()
    
    def motor_stop(self): #停止（R＋L）
        self.motor_r_stop()
        self.motor_l_stop()
