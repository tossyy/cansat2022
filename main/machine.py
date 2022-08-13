# 全てが使える条件を想定。

import smbus #気圧センサの管理に使います
import time
import struct
import statistics
import math
import csv
from motor import Motor
from arduino import Arduino
from nine import Nine
from pressure import Pressure
from gps import GPS
from light import Light
from jump import Jump
from camera import Camera

class Machine: #機体

    # 能代宇宙科学研究所仕様
    m_par_lat = 111319.491
    m_par_lng = 85078.906 

    target_position_path = '/home/pi/utat/log/target_posision.txt'
    mag_value_raw_path = '/home/pi/utat/log/mag_value_raw.csv'
    mag_value_corrected_path = '/home/pi/utat/log/mag_value_corrected.csv'

    def __double_to_hex(f):
        return hex(struct.unpack('>Q', struct.pack('>d', f))[0])

    def __init__(self):

        # 開始時間を記録
        self.start_time = time.perf_counter()

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

        # キャメラ初期化
        self.camera = Camera()

        self.phase0_time = time.perf_counter()

        print("マシーン初期化完了")
        self.i2c.write_byte(self.arduino.ARDUINO_ADRESS, self.arduino.PHASE_END)
        self.i2c.write_byte(self.arduino.ARDUINO_ADRESS, 0)

    def phase1(self): # Phase1。暗闇判定。
        print("###################\n# phase1 start    #\n###################")
        self.i2c.write_byte(self.arduino.ARDUINO_ADRESS, self.arduino.PHASE_START)

        '''
        【暗闇判定】
        条件（以下のうちいずれかを満たせばOK）
        ①30秒間光センサが閾値を上回る
        ②360秒間経過する
        (暗いほど値が大きい)
        '''

        # 光を検知しているかどうかの閾値
        light_threshold = 400

        # 光の閾値を上回り続けているかのフラグ
        is_continue = False

        # スイッチが入った瞬間
        start_time = 0

        # センサーの取得値を保存する配列
        phase1_data = []
        phase1_data.append(['time_stamp', 'light_val', 'is_continue'])

        while True:
            # 値を取得し出力
            light_val = self.light.get_val()
            time_stamp = time.perf_counter()-self.start_time
            print("{:5.1f}| 光センサ:{:>3d}, 継続:{}".format(time_stamp, light_val, is_continue))
            phase1_data.append([time_stamp, light_val, int(is_continue)])
            self.i2c.write_byte(self.arduino.ARDUINO_ADRESS, self.arduino.PHASE_1)

            if is_continue:

                # 光が途切れていた場合、やり直し
                if light_val <= light_threshold:
                    is_continue = False
                    continue

                # 光の継続時間を測る
                tim = time.perf_counter() - start_time

                if tim > 30:
                    print("暗闇判定：ケース①")
                    break

            # 暗い場合（閾値を上回る）
            elif light_val > light_threshold:

                is_continue = True
                start_time = time.perf_counter()

            tim_case = time.perf_counter() - self.phase0_time
            if tim_case > 360:
                print("暗闇判定：ケース②")
                break

            time.sleep(0.3)

        with open('/home/pi/utat/log/phase1.csv', 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerows(phase1_data)

        print("###################\n# phase1 finished #\n###################")
        self.i2c.write_byte(self.arduino.ARDUINO_ADRESS, self.arduino.PHASE_END)

        

    def phase2(self): # Phase2。放出判定。
        print("###################\n# phase2 start    #\n###################")
        self.i2c.write_byte(self.arduino.ARDUINO_ADRESS, self.arduino.PHASE_START)

        '''
        【放出判定】
        条件（以下のうちいずれかを満たせばOK）
        ①フライトピンが外れている and 10秒間光を検知し続ける
        ②30秒間光を検知し続ける
        '''

        # 光を検知しているかどうかの閾値
        light_threshold = 200

        # 光を検知し続けているかのフラグ
        is_continue = False

        # 光を検知し始めた時間
        start_time = 0

        # センサーの取得値を保存する配列
        phase2_data = []
        phase2_data.append(['time_stamp', 'light_val', 'jump_val', 'jump_is_off', 'is_continue'])

        while True:
            # 値を取得し出力
            light_val = self.light.get_val()
            jump_is_off = self.jump.is_off()
            time_stamp = time.perf_counter()-self.start_time
            print("{:5.1f}| 光センサ:{:>3d}, ジャンパピン:{}, 継続:{}".format(time_stamp, light_val, jump_is_off, is_continue))
            phase2_data.append([time_stamp, light_val, int(jump_is_off), int(is_continue)])
            self.i2c.write_byte(self.arduino.ARDUINO_ADRESS, self.arduino.PHASE_1)


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

        self.phase2_time = time.perf_counter()

        with open('/home/pi/utat/log/phase2.csv', 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerows(phase2_data)

        print("###################\n# phase2 finished #\n###################")
        self.i2c.write_byte(self.arduino.ARDUINO_ADRESS, self.arduino.PHASE_END)

    def phase3(self): # 着地判定
        print("###################\n# phase3 start    #\n###################")
        self.i2c.write_byte(self.arduino.ARDUINO_ADRESS, self.arduino.PHASE_START)

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

        # センサーの取得値を保存する配列
        phase3_data = []
        phase3_data.append(['time_stamp', 'pressure_val', 'altitude_val', 'is_continue'])

        while True:
            # 値を取得し出力
            pressure_val = self.pressure.get_pressure()
            altitude_val = self.gps.get_position()['altitude']
            time_stamp = time.perf_counter()-self.start_time
            print("{:5.1f}| 気圧:{:7.3f}, 高度:{:6.3f}, 継続:{}".format(time_stamp, pressure_val, altitude_val, is_continue))
            phase3_data.append([time_stamp, pressure_val, altitude_val, int(is_continue)])


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

            
            tim_case2 = time.perf_counter() - self.phase2_time
            if tim_case2 > 30:
                print("着地判定：ケース②")
                break

            time.sleep(0.3)

        with open('/home/pi/utat/log/phase3.csv', 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerows(phase3_data)

        print("###################\n# phase3 finished #\n###################")
        self.i2c.write_byte(self.arduino.ARDUINO_ADRESS, self.arduino.PHASE_END)

    def phase4(self): # ニクロム線断線
        print("###################\n# phase4 start    #\n###################")
        self.i2c.write_byte(self.arduino.ARDUINO_ADRESS, self.arduino.PHASE_START)

        print("断線開始")
        self.i2c.write_byte(self.arduino.ARDUINO_ADRESS, self.arduino.NICROM_ON)
        time.sleep(3)
        self.i2c.write_byte(self.arduino.ARDUINO_ADRESS, self.arduino.NICROM_OFF)
        print("断線終了")
        print("10秒待機")
        time.sleep(10)

        print("###################\n# phase4 finished #\n###################")
        self.i2c.write_byte(self.arduino.ARDUINO_ADRESS, self.arduino.PHASE_END)


    def phase5(self): # キャリブレーション
        print("###################\n# phase5 start    #\n###################")
        self.i2c.write_byte(self.arduino.ARDUINO_ADRESS, self.arduino.PHASE_START)

        print("5秒前進")
        self.motor.func_forward()
        time.sleep(5)
        print("1秒ブレーキ")
        self.motor.func_brake()
        time.sleep(1)
        self.calibrate()

        print("###################\n# phase5 finished #\n###################")
        self.i2c.write_byte(self.arduino.ARDUINO_ADRESS, self.arduino.PHASE_END)

    def phase6(self):
        print("###################\n# phase6 start    #\n###################")
        self.i2c.write_byte(self.arduino.ARDUINO_ADRESS, self.arduino.PHASE_START)

        # センサーの取得値を保存する配列
        phase6_data = []
        phase6_data.append(['time_stamp', 'latitude', 'longitude', 'theta', 'distance'])
        
        with open(self.target_position_path, mode='r') as f:
            lines = [s.strip() for s in f.readlines()]
            target_latitude = float(lines[0])
            target_longitude = float(lines[1])
        
        dist = lambda latitude, longitude: math.sqrt(((latitude-target_latitude)*self.m_par_lat)**2 + ((longitude-target_longitude)*self.m_par_lng)**2)

        #スタック判定用カウンター
        forward_counter = 0
        right_counter = 0
        left_counter = 0
        forward_sequence = True

        phase6_is_continue = True
        

        while phase6_is_continue:
            
            # gps が取れない時のやつ
            gps_start = time.perf_counter()

            while True:
                current_position = self.gps.get_position()
                latitude = current_position['latitude']
                longitude = current_position['longitude']
                if gps_start - time.perf_counter() > 40:
                    phase6_is_continue = False
                    break
                if latitude == 0 or longitude == 0:
                    continue
                break


            distance = dist(latitude, longitude)

            if distance < 1:
                break

            dif_arg = 999

            while abs(dif_arg) > math.pi/6:

                # スタック判定
                if len(phase6_data) > 4 and (right_counter > 3 or left_counter > 3 or forward_counter > 3):
                    dist_dif = abs(phase6_data[-3][4] - distance)
                    if dist_dif < 0.1:
                        print("dist_dif:{} -> 後退して旋回".format(dist_dif))
                        self.motor.func_back(speed=100)
                        time.sleep(2)
                        self.motor.func_right(speed=100)
                        time.sleep(2)
                        self.motor.func_forward(speed = 100)
                        time.sleep(2)
                        forward_counter = 0
                        right_counter = 0
                        left_counter = 0

                mag = self.nine.get_mag_value_corrected()

                phai_calc_continue = True
                theta_calc_continue = True

                while phai_calc_continue or theta_calc_continue:
                    try:
                        phai = math.atan(((target_latitude-latitude)*self.m_par_lat) / ((target_longitude-longitude)*self.m_par_lng))
                        phai_calc_continue = False

                    except ZeroDivisionError as e:
                        print(e)
                        self.motor.func_right()
                        time.sleep(0.5)

                        # gps が取れない時のやつ
                        gps_start = time.perf_counter()

                        while True:
                            current_position = self.gps.get_position()
                            latitude = current_position['latitude']
                            longitude = current_position['longitude']
                            if gps_start - time.perf_counter() > 40:
                                phase6_is_continue = False
                                break
                            if latitude == 0 or longitude == 0:
                                continue
                            break


                    try:
                        theta = math.atan(mag[0]/mag[1])
                        theta_calc_continue = False
                    
                    except ZeroDivisionError as e:
                        print(e)
                        self.motor.func_right()
                        time.sleep(0.5)
                        mag = self.nine.get_mag_value_corrected()
                    

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
                
                time_stamp = time.perf_counter()-self.start_time
                print("{:5.1f}| φ:{}, θ:{}, φ-θ:{}, latitude:{}, longitude:{}, distance:{}".format(time_stamp, phai, theta, dif_arg, latitude, longitude, distance))
                phase6_data.append([time_stamp, latitude, longitude, theta, distance])

                with open('/home/pi/utat/log/phase6.csv', 'w') as f:
                    writer = csv.writer(f, lineterminator='\n')
                    writer.writerows(phase6_data)
                    
                if dif_arg > 0:
                    self.motor.func_left(speed = 25)
                    time.sleep(dif_arg)
                    self.motor.func_brake()
                    left_counter += 1
                    forward_counter = 0
                    right_counter = 0
                    print("left")
                    forward_sequence = False
                    
                else:
                    self.motor.func_right(speed = 25)
                    time.sleep(abs(dif_arg))
                    self.motor.func_brake()
                    right_counter += 1
                    forward_counter = 0
                    left_counter = 0
                    print("right")
                    forward_sequence = False
            
            self.motor.func_forward()
            forward_time = dist(latitude, longitude)/10 / 0.5
            if forward_time < 8:
                time.sleep(dist(latitude, longitude)/10 / 0.5) #暫定の0.5m/s。モーターのクラス変数にスピード追加して。！！！
            else:
                time.sleep(8)
            self.motor.func_brake()
            if forward_sequence:
                forward_counter += 1
                left_counter = 0
                right_counter = 0
            print("forward")


        print("###################\n# phase6 finished #\n###################")
        self.i2c.write_byte(self.arduino.ARDUINO_ADRESS, self.arduino.PHASE_END)

    def phase7(self): # キャメラ
        print("###################\n# phase7 start    #\n###################")
        self.i2c.write_byte(self.arduino.ARDUINO_ADRESS, self.arduino.PHASE_START)
        file_No = 0
        pre_res = None

        # スタック判定用諸量
        with open(self.target_position_path, mode='r') as f:
            lines = [s.strip() for s in f.readlines()]
            target_latitude = float(lines[0])
            target_longitude = float(lines[1])

        dist = lambda latitude, longitude: math.sqrt(((latitude-target_latitude)*self.m_par_lat)**2 + ((longitude-target_longitude)*self.m_par_lng)**2)

        forward_counter = 0
        rotation_counter = 0

        phase7_data = []
        phase7_data.append(['time_stamp','latitude','longitude','theta', 'distance'])

        while True:

            file_path = '/home/pi/utat/log/img/image{:>03d}.jpg'.format(file_No)
            file_No += 1

            print("taking pic...: {}".format(file_path))
            self.camera.take_pic(file_path) # 写真を撮る
            res = self.camera.detect_center(file_path) # 赤の最大領域の占有率と重心を求める

            # スタック判定
            # ①cansatの向きの計測
            mag = self.nine.get_mag_value_corrected()
            theta = math.atan(mag[0]/mag[1])

            # ②cansatとゴールの距離測定
            current_position = self.gps.get_position()
            latitude = current_position['latitude']
            longitude = current_position['longitude']

            distance = dist(latitude, longitude)

            time_stamp = time.perf_counter()-self.start_time

            phase7_data.append([time_stamp, latitude, longitude, theta, distance])

            if len(phase7_data) > 4:
                distance_dif = abs(phase7_data[-3][4] - distance)
                argument_dif = abs(phase7_data[-3][3] - theta)
                if (distance_dif < 0.05 and forward_counter > 3) or (argument_dif < math.pi/6 and rotation_counter > 3):
                    print("distance_dif:{} | argument_dif:{} -> 後退して旋回".format(distance_dif, argument_dif))
                    self.motor.func_back(speed=100)
                    time.sleep(2)
                    self.motor.func_right(speed=100)
                    time.sleep(2)

            if res['percent'] < 0.0005: # 赤の領域が少ない場合は、旋回する
                print("赤の領域微小のため右に1秒旋回")
                self.motor.func_right()
                time.sleep(1)
                self.motor.func_brake()
                forward_counter = 0
                rotation_counter += 1
                continue

            if res['percent'] > 0.70: # 赤の領域が大きい場合は、終了する
                print("赤の領域が70%以上となったため終了")
                break

            # 旋回すべき角度
            dif_arg = res['center'][0] * math.pi/6

            # ログの出力
            print('percent={}, center={}, dif_arg={}'.format(res['percent'], res['center'], dif_arg))
            
            # ずれ角度に合わせて旋回する
            if dif_arg > 0:
                self.motor.func_left()
                time.sleep(dif_arg)
                self.motor.func_brake()
                
            else:
                self.motor.func_right()
                time.sleep(abs(dif_arg))
                self.motor.func_brake()

            # 前進する
            self.motor.func_forward()
            time.sleep(2)
            self.motor.func_brake()
            forward_counter += 1
            rotation_counter = 0

        print("###################\n# phase7 finished #\n###################")
        self.i2c.write_byte(self.arduino.ARDUINO_ADRESS, self.arduino.PHASE_END)

    def calibrate(self):
        print("caliblation start")
        x_list = []
        y_list = []
        gx_list = []
        gy_list = []
        interval = 0.3
        around_time = 3
        N = int(around_time/interval)
        start_time = time.perf_counter()

        #15秒間，値を取る
        self.motor.func_right(speed=90)
        while time.perf_counter() - start_time < 15:
            mag_value = self.nine.get_mag_value()
            x_list.append(mag_value[0])
            y_list.append(mag_value[1])
            
            time.sleep(interval)
        
        self.motor.func_brake()
        
        for i in range(len(x_list)-N):
            gx_list.append(sum(x_list[i:i+N])/ N)
            gy_list.append(sum(y_list[i:i+N])/ N)
        
        self.nine.correction_x = sum(gx_list) / len(gx_list)
        self.nine.correction_y = sum(gy_list) / len(gy_list)

        x_list_corrected = [v - self.nine.correction_x for v in x_list]
        y_list_corrected = [v - self.nine.correction_y for v in y_list]

        with open(self.mag_value_raw_path, mode='w') as f:
            writer = csv.writer(f)
            for x,y in zip(x_list, y_list):
                writer.writerow([x, y])
        
        with open(self.mag_value_corrected_path, mode='w') as f:
            writer = csv.writer(f)
            for x,y in zip(x_list_corrected, y_list_corrected):
                writer.writerow([x, y])

        print("caliblation finish")


    def remember_gps(self):
        print('-----位置情報取得開始-----')
        time.sleep(5)
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
            
        with open(self.target_position_path, mode='w') as f:
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
            self.phase6()
            self.phase7()

        except Exception as e:
            print(e)

        finally:
            self.close()

if __name__ == "__main__":
    ma = Machine()
    try:
        time.sleep(5)
        ma.phase5()
        ma.phase6()
        ma.phase7()

    except Exception as e:
        print(e)
    finally:
        ma.close()
