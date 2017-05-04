import serial

class MetabotV2():
	def __init__(self, rfcomm):
		self.serial = serial.Serial(port=rfcomm, baudrate=115200)

	def start(self):
		self.serial.write('start\n\r'.encode('utf-8'))
		self.serial.flushInput()

	def control(self,x,y,theta):
		self.serial.write(('dx {}\n\r'.format(x)).encode('utf-8'))
		self.serial.flushInput()
		self.serial.write(('dy {}\n\r'.format(y)).encode('utf-8'))
		self.serial.flushInput()
		self.serial.write(('turn {}\n\r'.format(theta)).encode('utf-8'))
		self.serial.flushInput()

	def stop(self):
		self.serial.write('stop\n\r'.encode('utf-8'))
		self.serial.flushInput()
