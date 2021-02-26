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


		self.__infect_person__(self.Students[0])
		self.__infect_person__(self.Students[1000])

		self.start_sim()

	def start_sim(self):
		self.simulation(no_of_days=5)

def StartSimulation(pm):
	m = Master(pm)
	m.initiate()
