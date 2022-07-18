from machine import Machine

ma = Machine()
ma.motor.change_speed(30)
ma.calibrate(ma.motor)

while True:
    c = input()
    if c == "q":
        break
    if c == "a":
        mag_value = ma.nine.get_mag_value_corrected()
        print(mag_value)

ma.close()