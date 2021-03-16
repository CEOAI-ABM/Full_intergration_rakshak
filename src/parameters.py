import json
import random
import numpy as np
import pandas as pd
import geopandas as GP
import matplotlib.pyplot as plt
import mysql.connector
from shapely.geometry import Polygon, Point
from .map_utils import random_points_in_polygon, cal_coordinates

slots = json.load(open('data/Timetable/Schedule/slots.json'))

class Virus_Parameters:
	"""
	All virus related parameters
	"""

	def __init__(self, **kwargs):

		self.Virus_Name 			    = "CoronaVirus"
		self.Virus_R0 				    = kwargs.get("Virus_R0", 2.0)
		self.Initial_Compliance_Rate 	= kwargs.get("Initial_Compliance_Rate", 0.8)

		self.Virus_Params = kwargs.get("Virus_Params",
			'Transport' : {'Time':1,    'Distance':1},
			'Home' 		: {'Time':16,   'Distance':1},
			'Grocery'	: {'Time':0.5,  'Distance':4},
			'Unemployed': {'Time':8,    'Distance':1},
			'Random'	: {'Time':1,    'Distance':2},
			)

		self.Virus_DistanceDist 		= {"Constant": 0.128, "Ratio": 2.02}
		self.Virus_Deathrates 			= kwargs.get("Virus_Deathrates", [0.01/2,0.005/2,0.01/2,0.01/2,0.04/2,0.30/2]) # Between age groups in agedist model
		self.Virus_IncubationPeriod		= kwargs.get("Virus_IncubationPeriod", [6,6,8,5,2,2]) # Between Age groups
		self.Virus_ExpectedCureDays		= kwargs.get("Virus_ExpectedCureDays", 14) # Days to cure
		self.Virus_FullCapRatio 		= kwargs.get("Virus_FullCapRatio", [5/3,5/3,5/3]) # When hopitals are overwhelmed by how much propertion deathrateincreases
		self.Virus_PerDayDeathRate		= [EE/self.Virus_ExpectedCureDays for EE in self.Virus_Deathrates]
		self.Virus_ProbSeverity 		= kwargs.get("Virus_ProbSeverity", [[0.70,0.26,0.04],
																			[0.80,0.16,0.04],
																			[0.80,0.16,0.04],
																			[0.95,0.04,0.01],
																			[0.60,0.30,0.10],
																			[0.40,0.40,0.20],
																			[0.10,0.40,0.50]])  # Mild, Medicore, Severe between Age Groups

		self.Comorbidty_matrix = {
		'ComorbidX' 	: kwargs.get("Virus_Deathrates", [0.00,0.00,0.00,0.00,0.00,0.00] )	# Percentage of Population getting deasese X
		}

		self.Comorbidty_weights = {#self.pm.duration
		'ComorbidX' 	: [0.1,0.7,0.2] 					# Probablity of increase in Severtiy if you have Disease X
		}

class Spatial_Parameters:
	"""
	All campus map related parameters
	"""
	def __init__(self, ShpFile, OtherFile):

		self.Departments                                = ['AE', 'AG', 'AR', 'BT', 'CE', 'CH',
														   'CS', 'CY', 'EC', 'EE', 'EX', 'GG',
														   'HS', 'IE', 'IM', 'MA', 'ME', 'MF',
														   'MI', 'MT', 'NA', 'PH', 'QE', 'QM']

		self.sectors 									= ['Academic', 'Residence', 'Restaurant',
															'Healthcare', 'Market', 'Gymkhana',
															'Grounds', 'Non_Academic']



		self.Number_Workers                             = []
		self.Floor                                      = []
		self.Daily_People_Expectation                   = []

		gdf                                             = GP.read_file(ShpFile)
		self.df                                         = pd.read_csv(OtherFile,na_filter=False)
		self.building_name                              = gdf['name']
		self.rooms_packing_fraction                     = [1 for i in range(len(self.building_name))]
		self.description                                = gdf['descriptio']
		self.coordinates, self.ref, self.polygons       = cal_coordinates(gdf)
		self.rooms                                      = []
		self.num_rooms_per_floor                        = list()
		self.heights                                    = list()
		self.xlist = []
		self.ylist = []

		self.Population_groups 	=  [5,18,25,60,80,150]                   #Max ages of different groups

		self.__assign_num_rooms_heights__()

		self.__cal_rooms__(self.num_rooms_per_floor)

		self.__assign_coords__()

		self.__assign_remaining__()

		#self.pm = [self.num_rooms,[],[],self.xlist,self.ylist,[]] #(7 parameters to be returned to Sector())

	def __assign_remaining__(self):
		for i in range(len(self.building_name)):
			self.Number_Workers.append(np.random.randint(5,20))
			self.Floor.append([])

			for j in range(1, self.heights[i]+1):
				for k in range(self.num_rooms_per_floor[i]):
					self.Floor[i].append(j)

			self.Daily_People_Expectation.append(np.random.randint(0, 50, self.num_rooms_per_floor[i]*self.heights[i]))

	def __assign_num_rooms_heights__(self):
		'''
		assigns number of rooms by taking reference of the lib and lbs if not known  through KGP Data - Sheet1.csv
		and randomly allocates no of floors if not known through KGP Data - Sheet1.csv
		'''

		lib_area                          = self.polygons[2].area #area of library
		lib_num_rooms_per_floor           = 60
		lbs_area                          = self.polygons[32].area #area of LBS Hall
		lbs_num_rooms_per_floor           = 650

		for i in range(len(self.building_name)):
			try:
				self.num_rooms_per_floor.append(int(self.df['number of rooms/floor'][i]))
				self.heights.append(int(self.df['height'][i]))
			except:
				if self.df['description'][i] == 'Academic':
					mu = lib_num_rooms_per_floor*self.polygons[i].area/lib_area
				else:
					mu = lbs_num_rooms_per_floor*self.polygons[i].area/lbs_area
				self.num_rooms_per_floor.append(int(abs(np.round(np.random.normal(mu,3,1)))))
				if self.num_rooms_per_floor[-1] == 0:
					self.num_rooms_per_floor[-1] = 1
				self.heights.append(int(abs(np.round(np.random.normal(3,0.5,1)))))

	def __assign_coords__(self):
		j = 0
		for buil in self.rooms:
			self.xlist.append([i.x for i in buil]*self.heights[j])
			self.ylist.append([i.y for i in buil]*self.heights[j])
			j+=1

	def __cal_rooms__(self, no_rooms):
		for i in range(len(self.building_name)):
			points = random_points_in_polygon(no_rooms[i],self.polygons[i])
			self.rooms.append(points)
		return

class Parameters(Virus_Parameters, Spatial_Parameters):
	"""
	All Parameters
	"""
	def __init__(self, **kwargs):

		ShpFile = kwargs.get("ShpFile", "")
		OtherFile = kwargs.get("OtherFile", "")

		Virus_Parameters.__init__(self, **kwargs)
		Spatial_Parameters.__init__(self, ShpFile, OtherFile)
		self.SIM_DAYS=5;

		self.SIM_DAYS = kwargs.get("SIM_DAYS", 5)

class Contact_Graph_Parameters:
	def __init__(self, db_conn=None):
		self.duration 		= 14 # in days
		self.infectdist		= 0.005 # in metres (infection radius, default value keep around 10)
		self.tstep 			= 3600 # the current timestep for activity data in seconds
		self.units 			= 10 #  maximum allowed units of tstep missing from the geo-coordinates data for imputation

if __name__=='__main__':
	ShpFilePath = "../data/shapes/kgpbuildings.shp"
	FilePath = "../data/Campus_data/KGP Data - Sheet1.csv"
	pm = Parameters(ShpFilePath,FilePath)
	k = 0
	while True:
		try:
			print(k,pm.building_name[k],"---- DESCRIPTION:",pm.description[k],"---- Number of Rooms per Floor:",pm.num_rooms_per_floor[k],"---- Heights of the building",pm.heights[k])
			k+=1
		except:
			break
