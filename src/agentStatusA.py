class AgentStatusA():
	"""docstring for AgentStatus"""
	status  = ['Free','Quarentined','Out_of_campus','Hospitalized','ICU','Isolation']

	def __init__(self):
		self.IN_Campus			    = True
		self.Status 				= self.status[0]	
		
	def _left_(self):
		self.IN_Campus = False

	def _entered_(self):
		self.IN_Campus = True
		

	def leave_campus(self):
		acceptable_states	= [self.status[0]]
		assert self.Status in acceptable_states
		self.Status  		= self.status[2]


	def enter_campus(self):
		acceptable_states	= [self.status[2]]
		assert self.Status in acceptable_states
		self.Status  		= self.status[0]

	def quarentined(self):
		acceptable_states	= [self.status[0],self.status[1],self.status[2]]
		assert self.Status in acceptable_states
		
		self.Status  		= self.status[1]

	def hospitalized(self):

		acceptable_states	= [self.status[0],self.status[1]]
		assert self.Status in acceptable_states

		self.Status  		= self.status[3]


	def admit_icu(self):
		acceptable_states	= [self.status[0],self.status[1],self.status[3]]
		assert self.Status in acceptable_states

		self.Status  		= self.status[4]

	def isolate(self):
		acceptable_states	= [self.status[0],self.status[1],self.status[3],self.status[4],self.status[5]]
		assert self.Status in acceptable_states

		self.Status  	= self.status[5]

	def is_Free(self):
		return self.Status == self.status[0]
	def is_Quarentined(self):
		return self.Status == self.status[1]
	def is_Out_of_campus(self):
		return self.Status == self.status[2]
	def is_Hospitalized(self):
		return self.Status == self.status[3]
	def is_ICU(self):
		return self.Status == self.status[4]
	def is_Isolation(self):
		return self.Status == self.status[5]
    
class AgentStateA():
	"""docstring for AgentStateA"""
	states  = ['Healthy','Asymptomatic','Symptomatic','Recovered','Died']

	def __init__(self):
		self.State 			= self.states[0]	

		
	def infected(self):
		acceptable_states	= [self.states[0]]
		assert self.State in acceptable_states
		self.State  		= self.states[1]


	def show_symptoms(self):
		acceptable_states	= [self.states[1],self.states[2]]
		assert self.State in acceptable_states
		self.State  		= self.states[2]

	def recover(self):
		acceptable_states	= [self.states[2]]
		assert self.State in acceptable_states
		self.State  		= self.states[3]


	def die(self):
		acceptable_states	= [self.states[2]]
		assert self.State in acceptable_states
		self.State  		= self.states[4]

	def is_Healthy(self):
		return self.State == self.states[0]
	def is_Asymptomatic(self):
		return self.State == self.states[1]
	def is_Symptomatic(self):
		return self.State == self.states[2]
	def is_Recovered(self):
		return self.State == self.states[3]
	def is_Died(self):
		return self.State == self.states[4]
