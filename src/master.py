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
		print(self.Students[0].timetable)
		print(self.Profs[0].timetable)
		self.start_movement()

def StartSimulation(pm):
	m = Master(pm)
	print(m)
	m.initiate()
	print(m.Students[0].schedule)
	print(m.Profs[0].schedule)
