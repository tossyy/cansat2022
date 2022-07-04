from arduino import Arduino

class Light:

    def __init__(self, arduino):
        self.ad = arduino
        print("光センサー初期化完了")
    
    def get_val(self):
        return self.ad.get_light()