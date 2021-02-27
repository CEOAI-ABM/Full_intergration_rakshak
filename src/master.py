from .Campus_Model import Campus
from .virusmodel import TruthClassStatus

class Master(Campus):
	"""
	Handles all the initialization and eventually parallelization (if required)
	"""

	def __init__(self, pm):
		self.pm = pm

		super().__init__()

	def initiate(self):
		self.initialize_campus()
		
		self.SIM_DAYS = 10
		self.simulation()

def StartSimulation(pm):
	m = Master(pm)
	m.initiate()
