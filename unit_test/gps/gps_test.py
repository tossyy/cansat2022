import serial
import binascii
ser = serial.Serial('/dev/serial0', 115200, timeout = 0.5)  #UART初期化

#コマンド送信
ser.write(b'\x22\x00\x00\x22')　#4バイトのByte型でデータを送信
ser.write("hello")

#コマンドの結果を受信(4byte)
data = ser.read(4)
#コマンドの結果を受信
data = ser.readline() 　#区切り文字0x0Aまでのデータを受信

#binデータで読み出されるので結果をhexに変換
data=binascii.b2a_hex(data)

ser.close() # ポートのクローズ