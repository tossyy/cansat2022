import board
import busio
import time
 
i2c = busio.I2C(board.SCL, board.SDA)
 
while not i2c.try_lock():
    pass
 
i2c.writeto(0x5d, bytes([0x0f]), stop=False)
result = bytearray(1)
i2c.readfrom_into(0x5d, result)
print(result)
i2c.unlock()