import readchar
from motor import Motor

class Machine: #機体

    def __init__(self):
        # モーター初期化
        self.motor = Motor()
        

    def controll(self):

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

    def close(self):
        self.motor.close()

    def run(self):
        self.controll()
        self.close()

if __name__ == "__main__":
    machine = Machine()
    machine.run()