import time
import csv

from machine import Machine

val = int(input())
ma = Machine()

t_start = time.perf_counter()
ma.motor.change_speed(val)
ma.motor.func_right()

xs = []
ys = []

while time.perf_counter() - t_start < 20 :
    xs.append(ma.nine.get_mag_value()[0])
    ys.append(ma.nine.get_mag_value()[1])
    time.sleep(0.1)

with open("/home/pi/utat/calib_data.csv", "w") as f:
    csv_obj = csv.writer(f)
    csv_obj.writerow(xs)
    csv_obj.writerow(ys)







