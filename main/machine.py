from multiprocessing.dummy import current_process
import smbus #気圧センサの管理に使います
import time
import statistics
import math
import readchar
import RPi.GPIO as GPIO
from motor import Motor
# from nine import Nine
from pressure import Pressure
from gps import GPS
from light import Light
from jump import Jump

class Machine: #機体

    def __init__(self):
        # i2c初期化
        self.i2c = smbus.SMBus(1)

        # モーター初期化
        self.motor = Motor()

        # 9軸センサー初期化
        # self.nine = Nine(self.i2c)

        # 気圧センサー初期化
        self.pressure = Pressure(self.i2c)

        # 光センサー初期化
        self.light = Light(self.i2c)

        # GPS初期化
        self.gps = GPS()

        # ジャンパピン初期化
        self.jump = Jump(self.i2c)
        

    def phase1(self): # Phase 1。放出判定。
        self.i2c.write_byte(0x8, 1)
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
        
        # Phase 1 が終わった時刻を記録
        self.phase1_time = time.perf_counter()

        print("###################\n# phase1 finished #\n###################")

    def phase2(self): # 着地判定
        print("###################\n# phase2 start    #\n###################")

        '''
        【着地判定】
        条件（以下のいずれかを満たせばOK）
        ①20秒間、気圧変化が0.1hPa以内で、高度変化が0.1m以内
        ②放出判定から120秒経過
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
                if abs(statistics.mean(pressure_list) - pressure_val) > 0.1 or abs(statistics.mean(altitude_list) - altitude_val) < 0.1:
                    is_continue = False
                    pressure_list = []
                    altitude_list = []
                    continue

                # 時間を測る
                tim_case1 = time.perf_counter() - start_time

                if tim_case1 > 20:
                    print("着地判定：ケース①")
                    break

            # 継続条件を満たした場合
            elif abs(statistics.mean(pressure_list) - pressure_val) <= 0.1 or abs(statistics.mean(altitude_list) - altitude_val) <= 0.1:
                is_continue = True
                start_time = time.perf_counter()

            
            tim_case2 = time.perf_counter() - self.phase1_time
            if tim_case2 > 120:
                print("着地判定：ケース②")
                break

            time.sleep(0.3)
        
        self.i2c.write_byte(0x8, 0)
        time.sleep(1)
        self.i2c.write_byte(0x8, 1)

        print("###################\n# phase2 finished #\n###################")

    def phase3(self): # キャリブレーション
        print("###################\n# phase3 start    #\n###################")

        print("3秒前進する")
        self.motor.func_forward()
        time.sleep(3.0)        
        print("3秒ブレーキ")
        self.motor.func_brake()
        time.sleep(3.0)
        
        
        print("3秒右回転する")
        self.motor.func_right()
        time.sleep(3.0)
        print("3秒ブレーキ")
        self.motor.func_brake()
        time.sleep(3.0)

        print("###################\n# phase3 finished #\n###################")

    def phase4(self):
        print("###################\n# phase3 start    #\n###################")
        
        file_path = 'target_pisision.txt'
        with open(file_path, mode='r') as f:
            lines = [s.strip() for s in f.readlines()]
            target_latitude = float(lines[0])
            target_longitude = float(lines[1])
        
        dist = lambda latitude, longitude: math.sqrt((latitude-target_latitude)**2 + (longitude-target_longitude)**2)

        while True:
            current_position = self.gps.get_position()
            latitude = current_position['latitude']
            longitude = current_position['longitude']
            print("(latitude, longitude) = ({}, {})".format(latitude, longitude))

            if dist(latitude, longitude) < 0.1:
                break

            time.sleep(3.0)

        print("###################\n# phase3 finished #\n###################")


    def control(self):

        print("-----入力開始-----")

        states = ['Forward', 'Back', 'Turn Left', 'Turn Right', 'Stop']
        current_state = 'Stop'

        while True:
            c = readchar.readkey()

            if c == 'w' and current_state != states[0]:
                self.motor.func_forward()
                current_state = states[0]
            
            if c == 's' and current_state != states[1]:
                self.motor.func_back()
                current_state = states[1]
            
            if c == 'a' and current_state != states[2]:
                self.motor.func_left()
                current_state = states[2]

            if c == 'd' and current_state != states[3]:
                self.motor.func_right()
                current_state = states[3]

            if c == ' ' and current_state != states[4]:
                self.motor.func_brake()
                current_state = states[4]

            if c == 'q':
                break

    def remember_gps(self):
        print('-----位置情報取得開始-----')
        latitude_list = []
        longitude_list = []

        for i in range(10):
            position = self.gps.get_position()
            latitude_list.append(position['latitude'])
            longitude_list.append(position['longitude'])
        
        latitude = statistics.mean(latitude_list)
        longitude = statistics.mean(longitude_list)

        file_path = 'target_pisision.txt'
        with open(file_path, mode='w') as f:
            f.write(str(latitude) + '\n' + str(longitude))
        
        print('-----位置情報取得終了-----')

    def close(self):
        self.i2c.close()
        self.motor.close()

    def run(self):
        self.phase1()
        self.phase2()
        self.phase3()
        self.phase4()
        self.close()