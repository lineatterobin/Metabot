import serial

class MetabotV2():
	def __init__(self, rfcomm):
		self.serial = serial.Serial(port=rfcomm, baudrate=115200)
		self.started = False

	def start(self):
		print("Start")
		self.serial.write('start\n\r'.encode('utf-8'))
		self.serial.flushInput()
		self.started = True

	def check(self,command,value):
		if command == "freq":
			value = 0 if abs(value) < 0.3 else value
		elif command == "dx":
			value = 0 if abs(value) < 10 else value
		elif command == "dy":
			value = 0 if abs(value) < 10 else value
		elif command == "turn":
			value = 0 if abs(value) < 6 else value
		return value

	def control(self,order):
		value = str(order[1])
		for i in range(2,len(order)):
			val = self.check(order[0],order[i])
			value = value + " " + str(val)
		print((order[0],value))
		self.serial.write(('{} {}\n\r'.format(order[0],value)).encode('utf-8'))
		self.serial.flushInput()
		
	def stop(self):
		print("Stop")
		self.serial.write('stop\n\r'.encode('utf-8'))
		self.serial.flushInput()
		self.started = False
