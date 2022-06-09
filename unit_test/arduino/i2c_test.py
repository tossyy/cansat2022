import smbus
import time

bus = smbus.SMBus(1)
arduino = 0x8

try:
    while True:
        CdsVal = 0
        JumperVal = 0
        data = bus.read_i2c_block_data(arduino, 1, 5)
        CdsVal |= int(data[0])
        CdsVal <<= 8
        CdsVal |= int(data[1])
        CdsVal <<= 8
        CdsVal |= int(data[2])
        CdsVal <<= 8
        CdsVal |= int(data[3])

        JumperVal = data[4]

        print(CdsVal, JumperVal)
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\nCtrl+C")
except Exception as e:
    print(str(e))
finally:
    print("\nexit program")
    bus.close()