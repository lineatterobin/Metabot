import sys
import time
from inputs import get_gamepad
from ihm import *

class XBoxController():
	def __init__(self):
		self.quit_attempt = False

	def get_events(self, old_events):
		new_events = get_gamepad()
		
		absY = old_events[0]
		absX = old_events[1]
		absRY = old_events[2]
		absRX = old_events[3]
		absZ = old_events[4]
		absRZ = old_events[5]
		absHY = 0
		absHX = 0
		B_E = 0
		B_W = 0
		B_N = 0
		B_S = 0
		B_ST = 0
		B_SEL = 0
		B_TR = 0
		B_TL = 0
		B_THL = 0
		B_THR = 0
		B_MODE = 0

		events = old_events

		for event in new_events:
			if event.ev_type != "Sync" :
				if event.code == "BTN_MODE" and event.state == 1:
					B_MODE = event.state
				elif event.code == "ABS_RY":
					if abs(event.state - absRY) > 500:
						absRY = event.state
				elif event.code == "ABS_Y":
					if abs(event.state - absY) > 500:
						absY = event.state
				elif event.code == "ABS_RX":
					if abs(event.state - absRX) > 500:
						absRX = event.state
				elif event.code == "ABS_X":
					if abs(event.state - absX) > 500:
						absX = event.state
				elif event.code == "ABS_HAT0Y":
					absHY = event.state
				elif event.code == "ABS_HAT0X":
					absHX = event.state
				elif event.code == "ABS_Z":
					absZ = float(event.state)
				elif event.code == "ABS_RZ":
					absRZ = float(event.state)
				elif event.code == "BTN_EAST":
					B_E = event.state
				elif event.code == "BTN_WEST":
					B_W = event.state
				elif event.code == "BTN_NORTH":
					B_N = event.state
				elif event.code == "BTN_SOUTH":
					B_S = event.state
				elif event.code == "BTN_START":
					B_ST = event.state
				elif event.code == "BTN_SELECT":
					B_SEL = event.state
				elif event.code == "BTN_TR":
					B_TR = event.state
				elif event.code == "BTN_TL":
					B_TL = event.state
				elif event.code == "BTN_THUMBL" and event.state == 1:
					B_THL = event.state
					self.quit_attempt = event.state
				elif event.code == "BTN_THUMBR":
					B_THR = event.state
				events = (absY, absX, absRY, absRX, absZ, absRZ, absHY, absHX, B_E, B_W, B_N, B_S, B_ST, B_SEL, B_TR, B_TL, B_THL, B_THR, B_MODE)
		return events

if __name__ == '__main__':
	if(len(sys.argv)) == 2:
		ihm = IHMetabot(sys.argv[1])
		xboxc = XBoxController()
		old_events = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		old_orders = []
		while(not xboxc.quit_attempt):
			new_events = xboxc.get_events(old_events)
			new_orders = ihm.handle_events(new_events,ihm.metabot.mode)
			old_events = new_events
			ihm.send_orders(new_orders,old_orders)
			old_orders = new_orders
		ihm.leave()
		sys.exit()
	else:
		print("Usage")
		print("xboxctrlr.py <rfcomm>")
