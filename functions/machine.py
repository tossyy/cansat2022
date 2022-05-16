#動きの関数を入れます
import pigpio as pig

moter_r1 = 1
moter_l1 = 2
moter_r2 = 3
moter_l2 = 4

class Moter:

    def __init__(self, pi):
        self.pi = pi
        pi.set_mode(moter_r1, pig.OUTPUT)
        pi.set_mode(moter_l1, pig.OUTPUT)

    def moter_r_forward(self):
        self.pi.set()

class Machine:

    def __init__(self):
        self.pi = pig.pi()
        self.moter = Moter(self.pi)
        self.sensa_9 = Sensa_9(self.pi)
        self.sensa_ato = Sensa_ato(self.pi)

    def phase1():

    def run():
        phase1()
        print(owari)
        pahse2()