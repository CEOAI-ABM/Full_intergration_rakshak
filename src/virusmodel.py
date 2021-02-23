import random
import numpy as np
from tabulate import tabulate

from .contact_graph import getContacts

class TruthClassStatus:
    """
    Keeps track of all case statistics
	"""

	def __init__(self):
		super().__init__()

		self.AFreeP 		= []
		self.AQuarentinedP 	= []
		self.SIsolatedP 	= []
		self.SHospitalizedP = []
		self.SIcuP 			= []
		self.RRecoveredP 	= []
		self.RDiedP 		= []

class Virus_Model(TruthClassStatus):
    """
    All virus related routines
    """

    def __init__(self):

		self.Esymptomstime				= self.pm.Virus_IncubationPeriod
		self.CureTime 					= self.pm.Virus_ExpectedCureDays
		self.ProbSeverity 				= self.pm.Virus_ProbSeverity 

        # Day wise placeholder
		self.Symptom_placeholder 		= [ [] for i in range(30) ]
		self.Recovered_Placeholder 		= [ [] for i in range(60) ]
		self.Deaths_Placeholder 		= [ [] for i in range(60) ]
	
	def __infect_person__(self, person):
		"""
		State change of a person from healthy to infected

		Args:
			person (person): person ojbect

		Returns:
			int: 0 if person wasn't able to infect due to already infected or out of Region. 1 otherwise
		"""
		if person.is_Out_of_Campus() ==False:
			if person.is_Healthy() == True :
				Symptom = int(np.random.normal(self.Esymptomstime[person.AgeClass],self.Esymptomstime[person.AgeClass]/3))
				if Symptom < 0:
					Symptom = 0

				self.Symptom_placeholder[Symptom].append(person)
				person.infected()
				self.RepoRateSum+=1
				return 1
			else:
				return 0
		else:
			return 0

	def __get_contacts__(self, person):
		"""
		Function to get the contacts of a person on a particular day
		"""

		# Query MySQL database -> get contacts and their edge weights 
		# Format it appropriately
		pass
	
	def has_symptoms(self, person, cure:int):
		"""Subroutine to change the state of person to symptomatic

		Args:
			person (object): person object who has shown symptons
			cure (int): days after which the person would be cured
		"""
		if person.is_Out_of_Region():
			person.quarentined()
			return
			
		prob_severity 	= person.get_prob_severity(self.ProbSeverity[person.AgeClass])
		deathrate 	 	= person.get_death_rate(self.AgeDR[person.AgeClass])
		deathrate 		= self.apply_dr_multiplier(person, deathrate)

		choice = random.choices([person.quarentined, person.hospitalized, person.admit_icu], weights=prob_severity)[0]
		choice() 
		
		if person.is_Quarentined():
			person.show_symptoms()

		if self.TestingOn:
			self.put_to_test(person,"Fresh")
		
		if cure<0:
			cure = 0
		
		deathrate = self.apply_dr_multiplier(person,deathrate)

		sampledeaths = random.choices([True, False],[deathrate,1-deathrate],k=cure)
		# Died with probablity death rate, True if died on that day
		try: # Look for index of True , if present died before cure
			deathday = sampledeaths.index(True)
			self.Deaths_Placeholder[deathday].append(person) #Append Death Day
		except ValueError: 
			self.Recovers_Placeholder[cure].append(person) # If not found, all is false, append cureday

	def __daily_hospitals_check__(self):
		"""Checks for all people who are supposed to be cured or died today i.e reach terminal state of statemachine
		"""
		today_cured = self.Recovers_Placeholder.pop(0)
		for person in today_cured:	
			person.recover()

		today_died  = self.Deaths_Placeholder.pop(0)
		for person in today_died:	
			person.die()

	def __daily_symptoms_check__(self):
		"""Checks for people whose symptoms have shown today. These people either will go to ICU, Hospital or remain at home
		"""
		today_symptoms = self.Symptom_placeholder.pop(0)

		#print('In region {}, {} people are added to testing list'.format(self.Name, len(today_symptoms)))
		curearray 	= np.random.normal(self.CureTime, self.CureTime/3, size=len(today_symptoms))
		for i, person in enumerate(today_symptoms):
			self.has_symptoms(person,int(curearray[i]))

	def __daily_transmissions__(self):
		for person in self.AFreeP:
			contacts_idx = self.__get_contacts__(person)
			# For each contact get P(transmission) from calibration.py as a function of interperson distance and time of contact
			P_TR = 0.1 # Dummy value for now

			for idx in contacts_idx:
				contact = self.__get_person_obj__(idx=idx) # Add this function in Campus_Model
				infect_bool = random.choices([True, False], weights=[P_TR, 1-P_TR])[0]
				if (infect_bool):
					self.__infect_person__(contact)

	def daily_transmissions(self):
		self.__daily_hospitals_check__()
		self.__daily_symptoms_check__()
		self.__daily_transmissions__()

		self.Symptom_placeholder.append([])
		self.Deaths_Placeholder.append([])
		self.Recovers_Placeholder.append([])




