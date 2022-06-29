#coding:utf-8

#GPIOライブラリをインポート
import RPi.GPIO as GPIO

class Motor:

    def __init__(self):

        #ピン番号の割り当て方式を「コネクタのピン番号」に設定
        GPIO.setmode(GPIO.BCM)

        #使用するピン番号
        self.AIN1 = 10
        self.AIN2 = 9
        self.PWMA = 11

        self.BIN1 = 22
        self.BIN2 = 27
        self.PWMB = 17

        #各ピンを出力ピンに設定
        GPIO.setup(self.AIN1, GPIO.OUT, initial = GPIO.LOW)
        GPIO.setup(self.AIN2, GPIO.OUT, initial = GPIO.LOW)
        GPIO.setup(self.PWMA, GPIO.OUT, initial = GPIO.LOW)

        GPIO.setup(self.BIN1, GPIO.OUT, initial = GPIO.LOW)
        GPIO.setup(self.BIN2, GPIO.OUT, initial = GPIO.LOW)
        GPIO.setup(self.PWMB, GPIO.OUT, initial = GPIO.LOW)

        #PWMオブジェクトのインスタンスを作成
        #出力ピン：12,26  周波数：100Hz
        self.p_a = GPIO.PWM(PWMA,100)
        self.p_b = GPIO.PWM(PWMB,100)

        #PWM信号を出力
        self.p_a.start(0)
        self.p_b.start(0)

        #デューティを設定(0~100の範囲で指定)
        #速度は80%で走行する。
        val = 80

        #デューティ比を設定
        self.p_a.ChangeDutyCycle(val)
        self.p_b.ChangeDutyCycle(val)

    #ブレーキする関数
    def func_brake(self):
        GPIO.output(self.AIN1, GPIO.HIGH)
        GPIO.output(self.AIN2, GPIO.HIGH)
        GPIO.output(self.BIN1, GPIO.HIGH)
        GPIO.output(self.BIN2, GPIO.HIGH)


    #前進する関数
    def func_forward(self):
        GPIO.output(self.AIN1, GPIO.LOW)
        GPIO.output(self.AIN2, GPIO.HIGH)
        GPIO.output(self.BIN1, GPIO.LOW)
        GPIO.output(self.BIN2, GPIO.HIGH)


    #後進する関数
    def func_back(self):
        GPIO.output(self.AIN1, GPIO.HIGH)
        GPIO.output(self.AIN2, GPIO.LOW)
        GPIO.output(self.BIN1, GPIO.HIGH)
        GPIO.output(self.BIN2, GPIO.LOW)


    #右回転する関数
    def func_right(self):
        GPIO.output(self.AIN1, GPIO.LOW)
        GPIO.output(self.AIN2, GPIO.HIGH)
        GPIO.output(self.BIN1, GPIO.HIGH)
        GPIO.output(self.BIN2, GPIO.LOW)


    #左回転する関数
    def func_left(self):
        GPIO.output(self.AIN1, GPIO.HIGH)
        GPIO.output(self.AIN2, GPIO.LOW)
        GPIO.output(self.BIN1, GPIO.LOW)
        GPIO.output(self.BIN2, GPIO.HIGH)

    def close(self):
        #PWM信号を停止
        self.p_a.stop()
        self.p_b.stop()

        #GPIOを開放
        GPIO.cleanup()
    