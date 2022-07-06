from machine import Machine

ma = Machine()
ma.motor.change_speed(30)
ma.nine.calibrate(ma.motor)
