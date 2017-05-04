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
		absHY = old_events[6]
		absHX = old_events[7]
		B_E = old_events[8]
		B_W = old_events[9]
		B_N = old_events[10]
		B_S = old_events[11]
		B_ST = old_events[12]
		B_SEL = old_events[13]
		B_TR = old_events[14]
		B_TL = old_events[15]

		events = old_events

		for event in new_events:
			if event.ev_type != "Sync" :
				if event.code == "BTN_MODE" and event.state == 1:
					self.quit_attempt = event.state
				elif event.code == "ABS_RY":
					if abs(event.state - absRY) > 2500:
						absRY = event.state
				elif event.code == "ABS_Y":
					if abs(event.state - absY) > 2500:
						absY = event.state
				elif event.code == "ABS_RX":
					if abs(event.state - absRX) > 2500:
						absRX = event.state
				elif event.code == "ABS_X":
					if abs(event.state - absX) > 2500:
						absX = event.state
				elif event.code == "ABS_HATOY":
						absHY = event.state
				elif event.code == "ABS_HATOX":
						absHX = event.state
				elif event.code == "ABS_Z":
					if abs(event.state - absZ) > 5:
						absZ = event.state
				elif event.code == "ABS_RZ":
					if abs(event.state - absRZ) > 5:
						absRZ = event.state
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
				events = (absY, absX, absRY, absRX, absZ, absRZ, absHY, absHX, B_E, B_W, B_N, B_S, B_ST, B_SEL, B_TR, B_TL)
		return events

if __name__ == '__main__':
	if(len(sys.argv)) == 2:
		ihm = IHMetabot(sys.argv[1])
		xboxc = XBoxController()
		old_events = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		while(not xboxc.quit_attempt):
			new_events = xboxc.get_events(old_events)
			orders = ihm.handle_events(new_events)
			old_events = new_events
			ihm.send_orders(orders)
		ihm.leave()
		sys.exit()
	else:
		print("Usage")
		print("xboxctrlr.py <rfcomm>")
