import readchar
import sys
sys.path.append('../../main')
from motor import Motor

class Machine: #機体

    def __init__(self):

        # モーター初期化
        self.motor = Motor()

        print("マシーン初期化完了")

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
            
            if c == 'd' and current_state != states[2]:
                self.motor.func_left()
                current_state = states[2]

            if c == 'a' and current_state != states[3]:
                self.motor.func_right()
                current_state = states[3]

            if c == ' ' and current_state != states[4]:
                self.motor.func_brake()
                current_state = states[4]
            
            if c == 'c':
                self.motor.func_brake()
                v = int(input("変更後のスピード:"))
                self.motor.change_speed(v)

            if c == 'q':
                break

    def close(self):
        self.motor.close()

    def run(self):
        try:
            self.control()

        except Exception as e:
            print(e)

        finally:
            self.close()

if __name__ == '__main__':

    print("Machine setting up...")
    ma = Machine()
    print("Set up finished")

    ma.run()