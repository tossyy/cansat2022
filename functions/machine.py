import pigpio as pig

motor_r1 = 1
motor_l1 = 2
motor_r2 = 3
motor_l2 = 4
SENSA_9 = 5

class Motor:

    def __init__(self, pi):
        self.pi = pi
        pi.set_mode(motor_r1, pig.OUTPUT)
        pi.set_mode(motor_l1, pig.OUTPUT)

    def motor_r_forward(self):
        self.pi.write(motor_)

class Sensa_9:

    def __init__(self, pi):
        self.pi = pi



class Machine:

    def __init__(self):
        self.pi = pig.pi()
        self.motor = Motor(self.pi)
        self.sensa_9 = Sensa_9(self.pi)
        self.sensa_ato = Sensa_ato(self.pi)

    def phase1(self):


    def phase2(self):


    def run():
        phase1()
        print(owari)
        phase2()