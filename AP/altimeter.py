import time
import board
import busio
import adafruit_lidarlite
import _thread as thread

# sudo i2cdetect -y 0
# pip3 install adafruit-circuitpython-lidarlite

i2c = busio.I2C(board.SCL, board.SDA)


sensor = adafruit_lidarlite.LIDARLite(i2c)


# read_data
while True:
    try:
        
        print(sensor.distance)
    except RuntimeError as e:
        
        print(e)
    #time.sleep(1) 