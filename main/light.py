from arduino import Arduino

class Light:

    def __init__(self, i2c):
        self.ad = Arduino(i2c)
    
    def get_val(self):
        return self.ad.get_light()