import random
import numpy as np
from tabulate import tabulate

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

class Virusmodel(TruthClassStatus):
    """
    All virus related routines
    """

    def __init__(self):
        # Day wise placeholder
		self.Symptom_placeholder 		= [ [] for i in range(30) ]
		self.Recovered_Placeholder 		= [ [] for i in range(60) ]
		self.Deaths_Placeholder 		= [ [] for i in range(60) ]