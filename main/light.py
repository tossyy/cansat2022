from arduino import Arduino

class Light:

    def __init__(self, arduino):
        self.ad = arduino
    
    def get_val(self):
        return self.ad.get_light()