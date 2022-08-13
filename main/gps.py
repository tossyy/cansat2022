import serial
import micropyGPS
import threading

class GPS:
    def rungps(self): # GPSモジュールを読み、GPSオブジェクトを更新する
        while True:
            try:
                sentence = self.ser.readline().decode('utf-8') # GPSデーターを読み、文字列に変換する
            except UnicodeDecodeError:
                sentence = self.ser.readline().decode('utf-8') # GPSデーターを読み、文字列に変換する
            if sentence[0] != '$': # 先頭が'$'でなければ捨てる
                continue
            for x in sentence: # 読んだ文字列を解析してGPSオブジェクトにデーターを追加、更新する
                self.gps.update(x)

    def __init__(self):
        self.gps = micropyGPS.MicropyGPS(9, 'dd')
        self.ser = serial.Serial('/dev/ttyS0', 9600, timeout=10)
        self.ser.readline() # 最初の1行は中途半端なデーターが読めることがあるので、捨てる

        self.gpsthread = threading.Thread(target=self.rungps, args=()) # 上の関数を実行するスレッドを生成
        self.gpsthread.daemon = True
        self.gpsthread.start() # スレッドを起動

        print("GPS初期化完了")

    def get_position(self):
        return {'latitude': self.gps.latitude[0],
                'longitude': self.gps.longitude[0],
                'altitude': self.gps.altitude}