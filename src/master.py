from .Campus_Model import Campus
from .virusmodel import TruthClassStatus
import time

class Master(Campus):
	"""
	Handles all the initialization and eventually parallelization (if required)
	"""

	def __init__(self, pm):
		self.pm = pm

		super().__init__()

	def initiate(self):
		self.initialize_campus()

		self.SIM_DAYS = self.pm.SIM_DAYS
		self.simulation(start_time=time.struct_time((2021,1,4,0,0,0,0,4,0)))

def StartSimulation(pm):
	m = Master(pm)
	m.initiate()
