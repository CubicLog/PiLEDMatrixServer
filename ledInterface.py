import time
import sys, os

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

#------Change Dir------
dname = os.path.dirname(os.path.realpath(__file__))
os.chdir(dname)

image = Image.open("phoenixLimit64.png")

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'
#options.pwm_lsb_nanoseconds = int(input("Speed -> "))
options.pwm_lsb_nanoseconds = 70

matrix = RGBMatrix(options = options)

# Make image fit our screen.
image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)

matrix.SetImage(image.convert('RGB'))

try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)