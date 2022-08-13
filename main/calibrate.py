from machine import Machine
import time

ma = Machine()
# ma.motor.change_speed(25)
# ma.calibrate()

# while True:
#     c = input()
#     if c == "q":
#         break
#     if c == "a":
#         mag_value = ma.nine.get_mag_value_corrected()
#         print(mag_value)

ma.motor.func_right()
time.sleep(30)
ma.motor.func_brake()

ma.close()