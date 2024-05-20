from rgbmatrix import RGBMatrix, RGBMatrixOptions

class MatrixManager():
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols =  cols

        self.options = RGBMatrixOptions()
        self.options.rows = 64
        self.options.cols = 64
        self.options.chain_length = 1
        self.options.parallel = 1
        self.options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'
        #self.options.pwm_lsb_nanoseconds = 70
        self.options.pwm_lsb_nanoseconds = int(input("pwm_lsb_nanoseconds -> "))

        self.matrix = RGBMatrix(options=self.options)
    
    def set_image(self, image):
        self.matrix.SetImage(image, unsafe=False)