import pigpio as pig

motor_r1 = 1
motor_l1 = 2
motor_r2 = 3
motor_l2 = 4
SENSA_9 = 5

class Motor: #モーター

    def __init__(self, pi):
        self.pi = pi
        pi.set_mode(motor_r1, pig.OUTPUT) #各ピンを出力に設定
        pi.set_mode(motor_l1, pig.OUTPUT)
        pi.set_mode(motor_r2, pig.OUTPUT)
        pi.set_mode(motor_l2, pig.OUTPUT)

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

class Sensa_ato: #気圧センサ

    def __init__(self, pi):
        self.pi = pi

class Sensa_light: #光センサ

    def __init__(self, pi):
        self.pi = pi

class Gps: #GPS

    def __init__(self, pi):
        self.pi = pi


class Machine: #機体

    def __init__(self): #全ての機能を搭載
        self.pi = pig.pi()
        self.motor = Motor(self.pi)
        self.sensa_9 = Sensa_9(self.pi)
        self.sensa_ato = Sensa_ato(self.pi)
        self.sensa_light = Sensa_light(self.pi)
        self.gps = Gps(self.pi)


    def phase1(self):

    def phase2(self):

    def run(self):
        phase1()
        print("phase1 finish")
        phase2()
        print("phase2 finish")