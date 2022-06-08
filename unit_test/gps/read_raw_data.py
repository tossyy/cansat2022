from socket import timeout
import serial

ser = serial.Serial('/dev/ttyS0', 9600, timeout=10)
while True:
    line = ser.readline()
    print(line.decode('utf-8'))
ser.close()
