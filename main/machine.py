import smbus #気圧センサの管理に使います
import time
import statistics
import math
from motor import Motor
from arduino import Arduino
from nine import Nine
from pressure import Pressure
from gps import GPS
from light import Light
from jump import Jump

class Machine: #機体

    m_par_lat = 111092.7384
    m_par_lng = 81540.4864 #過去のものを流用

    def __init__(self):
        # i2c初期化
        self.i2c = smbus.SMBus(1)

        # モーター初期化
        self.motor = Motor()

        # Arduino初期化
        self.arduino = Arduino(self.i2c)

        # 9軸センサー初期化
        self.nine = Nine(self.i2c)

        # 気圧センサー初期化
        self.pressure = Pressure(self.i2c)

        # 光センサー初期化
        self.light = Light(self.arduino)

        # GPS初期化
        self.gps = GPS()

        # ジャンパピン初期化
        self.jump = Jump(self.arduino)

        print("マシーン初期化完了")
        

    def phase1(self): # Phase 1。放出判定。
        print("###################\n# phase1 start    #\n###################")

        '''
        【放出判定】
        条件（以下のうちいずれかを満たせばOK）
        ①フライトピンが外れている and 10秒間光を検知し続ける
        ②30秒間光を検知し続ける
        '''

        # 光を検知しているかどうかの閾値
        light_threshold = 400

        # 光を検知し続けているかのフラグ
        is_continue = False

        # 光を検知し始めた時間
        start_time = 0


        while True:
            # 値を取得し出力
            light_val = self.light.get_val()
            jump_is_off = self.jump.is_off()
            print("光センサ:{:3}, ジャンパピン:{}, 継続:{}".format(light_val, jump_is_off, is_continue))
            
            if is_continue:

                # 光が途切れていた場合、やり直し
                if light_val >= light_threshold:
                    is_continue = False
                    continue

                # 光の継続時間を測る
                tim = time.perf_counter() - start_time

                if tim > 30:
                    print("放出判定：ケース②")
                    break
                if tim > 10 and jump_is_off:
                    print("放出判定：ケース①")
                    break

            # 光を検知した場合
            elif light_val < light_threshold:

                is_continue = True
                start_time = time.perf_counter()
            
            time.sleep(0.3)

        self.phase1_time = time.perf_counter()

        print("###################\n# phase1 finished #\n###################")

    def phase2(self): # 着地判定
        print("###################\n# phase2 start    #\n###################")

        '''
        【着地判定】
        条件（以下のいずれかを満たせばOK）
        ①8秒間、気圧変化が0.1hPa以内で、高度変化が0.2m以内
        ②放出判定から30秒経過
        '''

        # 継続しているかどうかのフラグ
        is_continue = False

        # 継続開始時間
        start_time = 0

        pressure_list = []
        altitude_list = []

        while True:
            # 値を取得し出力
            pressure_val = self.pressure.get_pressure()
            altitude_val = self.gps.get_position()['altitude']
            print("気圧:{:.3f}, 高度:{}, 継続:{}".format(pressure_val, altitude_val, is_continue))

            pressure_list.append(pressure_val)
            altitude_list.append(altitude_val)

            if is_continue:

                # 継続が切れていた場合、やり直し
                if abs(statistics.mean(pressure_list) - pressure_val) > 0.1 or abs(statistics.mean(altitude_list) - altitude_val) > 0.2:
                    is_continue = False
                    pressure_list = []
                    altitude_list = []
                    continue

                # 時間を測る
                tim_case1 = time.perf_counter() - start_time

                if tim_case1 > 8:
                    print("着地判定：ケース①")
                    break

            # 継続条件を満たした場合
            elif abs(statistics.mean(pressure_list) - pressure_val) <= 0.1 or abs(statistics.mean(altitude_list) - altitude_val) <= 0.2:
                is_continue = True
                start_time = time.perf_counter()

            
            tim_case2 = time.perf_counter() - self.phase1_time
            if tim_case2 > 30:
                print("着地判定：ケース②")
                break

            time.sleep(0.3)

        print("###################\n# phase2 finished #\n###################")

    def phase3(self): # ニクロム線断線
        print("###################\n# phase3 start    #\n###################")
        print("断線開始")
        self.i2c.write_byte(self.arduino.ARDUINO_ADRESS, self.arduino.NICROM_ON)
        time.sleep(3)
        self.i2c.write_byte(self.arduino.ARDUINO_ADRESS, self.arduino.NICROM_OFF)
        print("断線終了")
        print("10秒待機")
        time.sleep(10)
        print("###################\n# phase3 finished #\n###################")


    def phase4(self): # キャリブレーション
        print("###################\n# phase4 start    #\n###################")
        print("5秒前進")
        self.motor.func_forward()
        time.sleep(5)
        print("1秒ブレーキ")
        self.motor.func_brake()
        time.sleep(1)
        self.nine.calibrate(self.motor)

        print("###################\n# phase4 finished #\n###################")

    def phase5(self):
        print("###################\n# phase5 start    #\n###################")
        
        file_path = '/home/pi/utat/target_posision.txt'
        with open(file_path, mode='r') as f:
            lines = [s.strip() for s in f.readlines()]
            target_latitude = float(lines[0])
            target_longitude = float(lines[1])
        
        dist = lambda latitude, longitude: math.sqrt(((latitude-target_latitude)*self.m_par_lat)**2 + ((longitude-target_longitude)*self.m_par_lng)**2)

        while True:
            current_position = self.gps.get_position()
            latitude = current_position['latitude']
            longitude = current_position['longitude']
            print("(latitude, longitude) = ({}, {})".format(latitude, longitude))

            if dist(latitude, longitude) < 5:
                break

            dif_arg = 999

            while abs(dif_arg) > math.pi/3:
                mag = self.nine.get_mag_value_corrected()
                phai = math.atan(((target_latitude-latitude)*self.m_par_lat) / ((target_longitude-longitude)*self.m_par_lng))
                theta = math.atan(mag[0]/mag[1])
                if target_longitude-longitude < 0:
                    phai += math.pi
                if phai < 0:
                    phai += 2*math.pi
                if mag[1] < 0:
                    theta += math.pi
                if theta < 0:
                    theta += 2*math.pi
                dif_arg = phai - theta
                if dif_arg > math.pi:
                    dif_arg = 2*math.pi - dif_arg
                if dif_arg < -math.pi:
                    dif_arg = -(2*math.pi + dif_arg)
                
                print("φ:{}, θ:{}, φ-θ:{}, latitude:{}, longitude:{}, distance:{}".format(phai, theta, dif_arg, latitude, longitude, dist(latitude, longitude)))

                self.motor.change_speed(40)
                if dif_arg > 0:
                    self.motor.func_left()
                    time.sleep(dif_arg)
                    self.motor.func_brake()
                    
                else:
                    self.motor.func_right()
                    time.sleep(abs(dif_arg))
                    self.motor.func_brake()
                    
                self.motor.change_speed(90)

                
                time.sleep(1)
            
            self.motor.func_forward()
            time.sleep(dist(latitude, longitude)/10 / 0.5) #暫定の0.5m/s。モーターのクラス変数にスピード追加して。！！！
            self.motor.func_brake()

        print("###################\n# phase5 finished #\n###################")
        

    def remember_gps(self):
        print('-----位置情報取得開始-----')
        latitude_list = []
        longitude_list = []

        for i in range(10):
            position = self.gps.get_position()
            lat = position['latitude']
            lon = position['longitude']
            if lat != 0 and lon != 0:
                latitude_list.append(lat)
                longitude_list.append(lon)
            print("({}, {})".format(position['latitude'], position['longitude']))
            time.sleep(1)
        
        if latitude_list != [] and longitude_list != []:
            latitude = statistics.mean(latitude_list)
            longitude = statistics.mean(longitude_list)
        else:
            latitude = 0
            longitude = 0


        file_path = '/home/pi/utat/target_posision.txt'
        with open(file_path, mode='w') as f:
            f.write(str(latitude) + '\n' + str(longitude))
        
        print('-----位置情報取得終了-----')

    def close(self):
        self.i2c.close()
        self.motor.close()

    def run(self):
        try:
            self.phase1()
            self.phase2()
            self.phase3()
            self.phase4()
            self.phase5()

        except Exception as e:
            print(e)

        finally:
            self.close()

if __name__ == "__main__":
    ma = Machine()
    try:
        time.sleep(5)
        ma.motor.change_speed(40)
        ma.nine.calibrate(ma.motor)
        ma.motor.change_speed(90)
        ma.phase5()
    except Exception as e:
        print(e)
    finally:
        ma.close()