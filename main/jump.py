from arduino import Arduino

class Jump:

    def __init__(self, arduino):
        self.ad = arduino
        print("ジャンパピン初期化完了")
    
    def is_off(self):
        return not self.ad.get_jump()