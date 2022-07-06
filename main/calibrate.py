from machine import Machine

ma = Machine()
ma.motor.change_speed(20)
ma.nine.calibrate(ma.motor)
