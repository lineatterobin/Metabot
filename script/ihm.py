import sys
import time
import random
from mbot import MetabotV2

class IHMetabot():
	"""Interface controller with metabot """
	def __init__(self,rfcomm):
		self.metabot = MetabotV2(rfcomm)
		self.even = True
		print("Connected")

	def handle_events(self,events):
		#Format controller output
		orders = []
		absY = events[0]
		absX = events[1]
		absRY = events[2]
		absRX = events[3]
		absZ = events[4]
		absRZ = events[5]
		absHY = events[6]
		absHX = events[7]
		B_S = events[8]
		B_N = events[10]
		B_W = events[9]
		B_E = events[11]
		B_ST = events[12]
		B_SEL = events[13]
		B_TR = events[14]
		B_TL = events[15]
		B_THL = events[16]
		B_THR = events[17]
		B_MODE = events[18]

		dx = (-absY//2000)*5
		dy = (absX//2000)*5
		dh = (B_TL*8 + B_TR*-8) if (B_TL + B_TR != 0) else 0 #Down if LR pressed Up if RR pressed
		turn = (absRX//2000)*2.5
		alt = (absZ/4 + 15)
		freq = (255-absRZ)/200

		if B_ST == 1 and not self.metabot.started:
			self.metabot.start()
		elif B_ST == 1 and self.metabot.started:
			self.metabot.stop()

		if self.metabot.mode == "trot":
			if B_MODE == 1:
				self.metabot.chmode("impro")
			if B_W == 1:
				self.metabot.crabVal = 30 - self.metabot.crabVal
				orders.append(("crab",self.metabot.crabVal))
			if B_N == 1:
				self.metabot.control(("toggleBackLegs", 0))
			if self.metabot.started:
				orders.append(("dx", dx))
				orders.append(("dy", dy))
				orders.append(("turn",turn))
				orders.append(("alt", alt))
				orders.append(("freq",freq))
				if dh != 0:
					orders.append(("h",self.metabot.h + dh))
		
		elif self.metabot.mode == "impro":
			if B_MODE == 1:
				self.metabot.chmode("trot")
			elif B_W == 1:
				orders.append(("Leg4",0))	
			elif B_N == 1:
				self.metabot.control(("Leg1",0))
			if B_E == 1:
				self.metabot.control(("Leg2",0))
			if B_S == 1:
				self.metabot.control(("Leg3",0))
			else:
				print(events)

		if absHX == -1:
			mid = random.randint(300,800)
			orders.append(("beepUntil", mid, 15000))
		elif absHY == 1:
			low = random.randint(50,350)
			orders.append(("beepUntil", low, 15000))
		elif absHY == -1:
			high = random.randint(700,2000)
			orders.append(("beepUntil", high, 15000))
		elif absHX == 1:
			orders.append(("beepUntil",42,0))
		return orders

	def send_orders(self,old_orders, new_orders):
		for new_order in new_orders:
			drop=False
			for old_order in old_orders:
				if old_order == new_order:
					drop=True
			if not drop:
				self.metabot.control(new_order)

	def leave(self):
		self.metabot.chmode("trot")
		self.metabot.stop()

	def impro(self):
		self.metabot.control(("Leg1",0))
		time.sleep(1)