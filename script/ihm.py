import sys
import time
from mbot import MetabotV2

class IHMetabot():
	"""Interface controller with metabot """
	def __init__(self,rfcomm):
		print("Start")
		self.metabot = MetabotV2(rfcomm)
		self.metabot.start()

	def handle_events(self,events):
		#Format controller output
		orders = ((events[1]//2000)*5, (events[0]//2000)*5, (events[3]//2000)*3)
		return orders

	def send_orders(self,orders):
		print(orders)
		self.metabot.control(orders[0],orders[1],orders[2])

	def leave(self):
		print("Stop")
		self.metabot.stop()
