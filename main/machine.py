from pickle import FALSE
import pigpio as pig #ピンの設定に使います
import smbus #気圧センサの管理に使います
import time
import statistics
from motor import Motor
from nine import Nine
from pressure import Pressure
from gps import GPS
from light import Light
from jump import Jump

class Machine: #機体

    def __init__(self):
        # i2c初期化
        self.i2c = smbus.SMBus(1)

        # ピン初期化
        self.pi = pig.pi()

        # モーター初期化
        self.motor = Motor(self.pi)

        # 9軸センサー初期化
        self.nine = Nine(self.i2c)

        # 気圧センサー初期化
        self.pressure = Pressure(self.i2c)

        # 光センサー初期化
        self.light = Light(self.i2c)

        # GPS初期化
        self.gps = GPS()

        # ジャンパピン初期化
        self.jump = Jump(self.i2c)

        # 光センサー初期化
        self.light = Light(self.i2c)
        

    def phase1(self): # Phase 1。放出判定。
        print("phase1 start")

        '''
        【放出判定】
        条件（以下のうちいずれかを満たせばOK）
        ①フライトピンが外れている and 10秒間光を検知し続ける
        ②30秒間光を検知し続ける
        '''

        # 光を検知しているかどうかの閾値
        light_threshold = 100

        # 光を検知し続けているかのフラグ
        is_continue = False

        # 光を検知し始めた時間
        start_time = 0


        while True:
            # 値を取得し出力
            light_val = self.light.get_val()
            jump_is_off = self.jump.is_off()
            print("光センサ:{}, ジャンパピン:{}".format(light_val, jump_is_off))
            
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

        print("phase1 finished")

    def phase2(self): # 着地判定
        print("phase2 start")

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
            print("気圧:{}, 高度:{}".format(pressure_val, altitude_val))

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

        print("phase2 finished")

    def close(self):
        self.i2c.close()

    def run(self):
        self.phase1()
        self.phase2()
        self.close()