import pigpio as pig

#ピン番号を設定
#数字は後で変更します
motor_r1 = 1 #モーターR（前進）
motor_l1 = 2 #モーターL（前進）
motor_r2 = 3 #モーターR（後退）
motor_l2 = 4 #モーターL（後退）
sensa_9_out = 5 #9軸センサ（出力）
sensa_9_in = 6 #9軸センサ（読取）
sensa_ato_out = 7 #気圧センサ（出力）
sensa_ato_in = 8 #気圧センサ（読取）
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

class Sensa_ato: #気圧センサ

    def __init__(self, pi):
        self.pi = pi
        self.pi.set_mode(sensa_ato_out, pig.OUTPUT)
        self.pi.set_mode(sensa_ato_in, pig.INPUT)

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
        self.sensa_ato = Sensa_ato(self.pi)
        self.sensa_light = Sensa_light(self.pi)
        self.gps = Gps(self.pi)


    def phase1(self):
        print("phase1 hajime")

    def phase2(self):
        print("phase2 hajime")
    
    def phase3(self):
        print("phase3 owari")

    def run(self):
        self.phase1()
        print("phase1 owari")
        self.phase2()
        print("phase2 owari")
        self.phase3()
        print("pfase3 owari")
