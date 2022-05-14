import pigpio as pig
import take_pic
import time

#ピンの設定

pi = pig.pi()

moter_r = 18
moter_l = 19

pi.set_mode(moter_r, pig.OUTPUT)
pi.set_mode(moter_l, pig.OUTPUT)


