
import csv

from machine import Machine

ma = Machine()

t_start = time.prefcounter()
ma.motor.speed_change(20)
ma.motor.func_right()

xs = []
ys = []

while time.prefcounter() - t_start < 20 :
    xs.append(ma.nine.get_mag_value()[0])
    ys.append(ma.nine.get_mag_value()[1])
    time.sleep(0.1)

with open("/home/pi/utat/calib_data.csv", "w") as f:
    csv_obj = csv.witter(f)
    csv_obj.writerow(xs)
    csv_obj.writerow(ys)







