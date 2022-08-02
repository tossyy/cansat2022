class Arduino:

    ARDUINO_ADRESS = 0x8
    NICROM_ON = 0x0
    NICROM_OFF = 0x1
    PHASE_START = 0x2
    PHASE_END = 0x3

    def __init__(self, i2c):
        self.i2c = i2c
        print("i2c初期化完了")
    
    def get_light(self):
        light_val = 0

        data = self.i2c.read_i2c_block_data(self.ARDUINO_ADRESS, 1, 5)
        light_val = (data[0]<<(8*3)) | (data[1]<<(8*2)) | (data[2]<<(8*1)) | (data[3]<<(8*0))
        
        return light_val
    
    def get_jump(self):
        jumper_val = 0

        data = self.i2c.read_i2c_block_data(self.ARDUINO_ADRESS, 1, 5)
        jumper_val = data[4]

        return jumper_val