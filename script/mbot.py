import serial
import time

class MetabotV2():
	def __init__(self, rfcomm):
		self.serial = serial.Serial(port=rfcomm, baudrate=115200)
		self.started = False
		self.mode = "trot"
		self.h = -55
		self.crabVal = 0
		self.l4 = False

	def start(self):
		print("Start")
		self.serial.write('start\r'.encode('utf-8'))
		self.serial.reset_input_buffer()
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
		elif command == "h":
			value = 0 if value > 0 else (-130 if value < -130 else value)
			self.h = value
		elif command == "alt":
			value = 45 if abs(value - 25) < 3 else value
		return value

	def control(self,order):
		value = str(self.check(order[0],order[1]))
		for i in range(2,len(order)):
			val = self.check(order[0],order[i])
			value = value + " " + str(val)
		print((order[0],value))
		self.serial.write(('{} {}\r'.format(order[0],value)).encode('utf-8'))
		self.serial.reset_input_buffer()
		
	def stop(self):
		print("Stop")
		self.serial.write('stop\r'.encode('utf-8'))
		self.serial.reset_input_buffer()
		self.started = False

	def chmode(self,mode):
		print("Mode " + mode)
		self.mode = mode
		self.serial.write(('{}\r'.format(mode)).encode('utf-8'))
		self.serial.reset_input_buffer()