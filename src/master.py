from .Campus_Model import Campus

class Master(Campus):
	"""
	Handles all the initialization and eventually parallelization (if required)
	"""
	
	def __init__(self, pm):
		self.pm = pm

		super(Master, self).__init__()
	
	def initiate(self):
		
		#self.initialize_campus()

def StartSimulation(pm):
	m = Master(pm)
	print(m)
	m.initiate()