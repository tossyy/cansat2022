from arduino import Arduino

class Jump:

    def __init__(self, arduino):
        self.ad = arduino
    
    def is_off(self):
        return not self.ad.get_jump()