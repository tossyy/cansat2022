from arduino import Arduino

class Jump:

    def __init__(self, i2c):
        self.ad = Arduino(i2c)
    
    def is_off(self):
        return not self.ad.get_jump()