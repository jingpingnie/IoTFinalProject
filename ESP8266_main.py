from machine import Pin,PWM,ADC,I2C,RTC,SPI
from ssd1306 import SSD1306_I2C
import network
from urequests import post
from ustruct import pack, unpack
from time import sleep, ticks_ms, ticks_diff
from json import dumps

# Define the button indicator
buttonC = Pin(2, Pin.IN)	# button press input
buttonA = Pin(3, Pin.IN)

# Define the default state of button begin pressed
global state
state = False

# Define the acceleration data string
global acceleration_x
global acceleration_y
global acceleration_z
global cnt

acceleration_x = []
acceleration_y = []
acceleration_z = []
cnt = 0

# Define Host IP address
Public_Host = 'http://3.16.31.183'# I2C Setup

# I2C Setup
i2c = I2C(-1, scl=Pin(5), sda=Pin(4))  # I2C initialization
oled = SSD1306_I2C(128, 32, i2c) #  interface through I2C
rtc = RTC()             #  use RTC to set the system time

# SPI Setup
spi = SPI(1, baudrate=500000, polarity=1, phase=1) # SPI initialization
spi.init()	# SPI initialization
cs = Pin(15, Pin.OUT)	# set up the chip select pin
cs.value(0)	# pull the chip select pin to ground by default

# Set up SPI registers
DEVID = 0x00 # device ID
POWER_CTL = 0x2D # power-saving features control
DATA_FORMAT = 0x31 # data format control
DATAX0 = 0x32 # x-axis data 0
DATAY0 = 0x34 # y-axis data 0
DATAZ0 = 0x36 # z-axis data 0

# Define calibration parameters
calibration_parameter = 0.0384 # earth gravitational acceleration devided by 255

sta_if = network.WLAN(network.STA_IF) # initialize wifi interface

if not sta_if.isconnected():
    print('connecting to network...')
    oled.fill(0) # clear screen
    oled.contrast(255) # turn the screen to its brightest setting
    oled.text('connecting...', 0, 0)
    oled.show()

    sta_if.active(True)
    sta_if.connect('Columbia University','')
    #sta_if.connect('LifeTime_Guest','')
    while not sta_if.isconnected():
        pass
print('network config: ', sta_if.ifconfig())
print('STA connection: ', sta_if.isconnected())

oled.fill(0) # clear screen
oled.contrast(255) # turn the screen to its brightest setting
oled.text('connected', 0, 0)
oled.show()


# Define the cursor location
# WE DON'T KNOW WHY BUT WE HAVE TO DECLARE THESE LOCATIONS AS GLOBAL VARIABLES OR OTHERWISE IT WON'T WORK.
global location_x
global location_y
global location_z

location_x = 0
location_y = 0
location_z = 0

# Define acceleration
accel_x = 0
accel_y = 0
accel_z = 0

# Write data through SPI
def SPI_W(address, data):
	address = address & 0x7F # make sure the first bit is 0 (for writing data)
	address = pack('b', address) # convert decimal address to binary
	data = pack('b', data) # convert decimal data to binary
	cs.value(0)	# pull the chip select pin low
	spi.write(address)
	spi.write(data)
	cs.value(1) # pull chip select pin high

# Read data (1 byte) through SPI
def SPI_R_1B(address):
	address = address | 0x80 # make sure the first bit is 1 (for reading data)
	address = pack('b', address) # convert decimal address to binary
	cs.value(0)	# pull the chip select pin low
	spi.write(address)
	data = spi.read(1)
	cs.value(1) # pull chip select pin high
	return data

# Read data (multiple bytes) through SPI
def SPI_R_nB(address):
	address = address | 0xC0 # make sure the first two bits are 11 (for reading multiple bytes of data)
	address = pack('b', address) # convert decimal address to binary
	cs.value(0)	# pull the chip select pin low
	spi.write(address)
	data = spi.read(2) # for our application we only read the first two bytes
	cs.value(1) # pull chip select pin high
	return data

# ADXL345 initialization
def init_ADXL345():
	SPI_W(POWER_CTL, 0x08) # turn the power-saving features control to the "measurement" mode

# Read x location
def read_accel_x():
	accel_x = SPI_R_nB(DATAX0)
	accel_x = unpack('h', accel_x)
	return accel_x[0] * calibration_parameter

# Read y location
def read_accel_y():
	accel_y = SPI_R_nB(DATAY0)
	accel_y = unpack('h', accel_y)
	return accel_y[0] * calibration_parameter

# Read z location
def read_accel_z():
	accel_z = SPI_R_nB(DATAZ0)
	accel_z = unpack('h', accel_z)
	return accel_z[0] * calibration_parameter

def button_press(self):
	global state

	print("trigger")
	sleep(0.1)

	state = True if state == False else False

	if state == False:
		pass

# Main function
def main():
	# initialize ADXL345
	init_ADXL345()
	
	# Assign an interrupt to the button press input
	buttonC.irq(trigger = (Pin.IRQ_RISING), handler = button_press)
	global state
	global location_x
	global location_y
	global location_z

	global acceleration_x
	global acceleration_y
	global acceleration_z
	global cnt

	while(1):
		if state == True:
			print('state=1')
			

			for i in range(0,20,1):

				accel_x = read_accel_x() # record the x-axis acceleration
				accel_y = read_accel_y() # record the y-axis acceleration
				accel_z = read_accel_z() # record the z-axis acceleration

				print('get acc x: ', accel_x)

				acceleration_x.append(str(accel_x));
				acceleration_y.append(str(accel_y));
				acceleration_z.append(str(accel_z));

				oled.fill(0) # clear screen
				oled.contrast(255) # turn the screen to its brightest setting
				oled.text('x: ' + str(accel_x), 0, 0)
				oled.text('y: ' + str(accel_y), 0, 8)
				oled.text('z: ' + str(accel_z), 0, 16)
				oled.show()
				sleep(0.005)

			print('lenth of data', len(acceleration_x))
			cnt += 1
			List = {"Character": "C",
					"Count": cnt,
					"DataLength": len(acceleration_x),
					"Data": {"Data_x": acceleration_x,
						 	 "Data_y": acceleration_y,
						 	 "Data_z": acceleration_z
						 }
				}
			print(acceleration_x)
			response = post(Public_Host, data=dumps(List))	
			print('Data posted, count: ',cnt)
			ratio = ''.join(response.text[0:5])
			oled.text('ratio: ' + str(ratio), 0, 24)
			oled.show()

			#state = False #while this line commented, send data until button pressed/ while not, send 50 sets of data
			acceleration_x = []
			acceleration_y = []
			acceleration_z = []
			List = {}


if __name__ == "__main__":
	main()