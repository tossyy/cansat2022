import pigpio as pg
import take_pic
import time

#ピンの設定

pi = pg.pi()

moter_r = 18
moter_l = 19

pi.set_mode(moter_r, pg.OUTPUT)
pi.set_mode(moter_l, pg.OUTPUT)


