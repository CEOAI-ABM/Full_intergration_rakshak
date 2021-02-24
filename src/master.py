from .Campus_Model import Campus
from .Campus_Units import Unit, Sector, Academic, Residence

class Master(Campus):
	"""
	Handles all the initialization and eventually parallelization (if required)
	"""
	
	def __init__(self, pm):
		self.pm = pm

		super().__init__()
	
	def initiate(self):
		self.initialize_campus()
		
		#print(self.Students[0].timetable)
		#print(self.Profs[0].timetable)
		#print(self.Staff[0].timetable)
		#print(self.sectors['Academic'].Units_list)
		self.start_sim()

	def start_sim(self):
		self.simulation(no_of_days=10)



def StartSimulation(pm):
	m = Master(pm)
	m.initiate()
