import os
import json
import time
import ctypes
import random
import numpy as np
import geopandas as GP
import matplotlib.pyplot as plt
from shapely.geometry import Point
import pandas as pd
import json
import csv

from .parameters import slots
from .statemachine import AgentStateA

# wifidata = json.load(open('data/Timetable/post5_probs.json'))
with open('data/survey_data/student.json') as fh:
	responses = json.load(fh)
surveydata = pd.read_csv("data/survey_data/Student Choices.csv")
with open("data/survey_data/hall_wise_place_weights.json") as fh:
	hall_wise_placeweights = json.load(fh)
with open("data/survey_data/year_wise_place_weights.json") as fh:
	year_wise_placeweights = json.load(fh)


class person(AgentStateA):
	""" Class for describing students
	Args:
		pm(object): parameter objects
		ID(int): ID of person
		role(str): student, faculty, staff
		dept(str): Department (Only applicable for students & faculty)
		inCampus(bool):
		year(int): only applicable for students
		schedule(dict): semester timetable for person
		master(object): master object
	"""

	def __init__(self, Campus=None, ID=0, dept=None, inCampus=True, age=-1, ageclass=-1, role=None, year=None, schedule=None, master=None, residence=None, Comorbidty_matrix=None):
		super(person,self).__init__()
		self.ID             = ID
		self.Age            = age
		self.AgeClass       = ageclass
		self.master         = master
		self.residence      = residence
		self.Campus         = Campus
		self.inCapmus       = inCampus # Whether the person is currently in Campus
		self.Role           = role #  Namely student, faculty or staff
		self.dept           = dept
		self.today_schedule = None

		self.timetable      = {"sunday": {}, "monday": {}, "tuesday": {}, "wednesday": {}, "thursday": {}, "friday": {}, "saturday": {}}

		self.Disease 		= []

		if Comorbidty_matrix!=None:
			self.__get_disease__(Comorbidty_matrix)

		self.update_objects(self.Campus)

	def get_schedule(self):
		pass

	def get_prob_severity(self,ProbSeverity):
		for i in self.Disease:
			ProbSeverity = ProbSeverity
		return ProbSeverity

	def __get_disease__(self, CM):
		for i in CM.items(): #Cm is comorbidity matrix
			probablity = [i[1][self.AgeClass],1-i[1][self.AgeClass]]
			has_disease = random.choices([True, False],weights=probablity)[0]
			if has_disease:
				self.Disease.append(i[0])

	def get_death_rate(self,deafaultDR):
		for i in self.Disease:
			deafaultDR = deafaultDR
		return deafaultDR

class student(person):
	def __init__(self,  Campus=None, ID=0, dept=None, inCampus=True, age=-1, ageclass=-1, role="student", year=None, schedule=None, master=None,residence=None, personal_choice=None):
		super().__init__(ID=ID, role=role, age=age, dept=dept, residence=residence)
		self.personID = dept+str(ID)
		self.Campus = Campus
		self.schedule = schedule
		self.year = year
		self.residence_building_id = self.residence[0]
		self.residence_unit  = self.Campus.Units_Placeholder[self.residence[0]][self.residence[1]+self.Campus.Index_Holder[self.residence[0]]]
		self.residence_point = self.residence_unit.location
		self.personal_choice = personal_choice
		self.get_timetable()

	def get_timetable(self):
		# print("entered get_timetable")
		for day in self.timetable:
			for i in range(24):
				#self.timetable[day][str(i)+'-'+str(i+1)]=self.Campus.ParamObj.building_name[self.residence_unit.Building]
				self.timetable[day][i]=self.residence_unit
				# if i >= 18 or i < 8:
				# 	weights = []
				# 	for key in wifidata:
				# 		weights.append(wifidata[key][day][str(i)+'-'+str(i+1)])
				# 	building_id = random.choices([i for i in range(self.Campus.Total_Num_Buildings)],weights)[0]
				# 	unit_id = random.choice(list(self.Campus.Units_Placeholder[building_id].keys()))
				# 	self.timetable[day][i] = self.Campus.Units_Placeholder[building_id][unit_id]

		for subject in self.schedule:
			class_room=self.schedule[subject]['room']
			slot_name=self.schedule[subject]['slot']
			#print(slot_name)
			for classes,times in slots[slot_name].items():
				#print(times[0]+' '+times[1])
				if len(slot_name)>3:
					timing=times[1].split('-')
					starting=int(timing[0])
					ending=int(timing[-1])
					for i in range(starting, ending):
						try:
							self.timetable[times[0]][i]=self.Campus.__room2unit__(class_room)
							self.Campus.__room2unit__(class_room).isclassroom = True
						except:
							altroom = sum([ord(char) for char in class_room])+self.Campus.Index_Holder[42]
							self.timetable[times[0]][i]=self.Campus.Units_Placeholder[42][altroom]
							self.Campus.Units_Placeholder[42][altroom].isclassroom = True
				else:
					self.timetable[times[0]][int(times[1].split('-')[0])]=self.Campus.__room2unit__(class_room)
					self.Campus.__room2unit__(class_room).isclassroom = True
		with open('data/survey_data/temp.csv', 'r',encoding="utf8") as file:
			reader1 = csv.reader(file)
			k=0
			building_name_to_id = {}
			building_id_to_name={}
			for row in reader1:
				building_name_to_id[row[0]] = int(row[1])
				building_id_to_name[int(row[1])] =row[0]
				k+=1


		l = len(responses[building_id_to_name[self.residence_building_id]][str(self.year)])
		if l == 0:
			return
		response_no = responses[building_id_to_name[self.residence_building_id]][str(self.year)][self.personal_choice%l]
		df_req = surveydata[surveydata["Unnamed: 0"] == response_no]
		#self.clustering has to be done
		no_of_weekdays = df_req.iloc[0,4]
		no_of_hours_weekdays = df_req.iloc[0,5]

		places_of_visit = []
		for i in df_req.iloc[0,6].split(";"):
			if building_name_to_id[i] == -1:
				continue
			places_of_visit.append(building_name_to_id[i])

		no_of_diff_places = df_req.iloc[0,7]

		sleep_time = df_req.iloc[0,12]
		if sleep_time == 'I usually stay in my room':
			sleep_time = 21
		else:
			sleep_time = int(sleep_time.split('-')[1][:-2])
			if sleep_time < 4:
				sleep_time += 24
			else:
				sleep_time+=12

		if df_req.iloc[0,10] != "Never": temp_times = list(map(lambda x: x.split("-"),df_req.iloc[0,10].split(";")))
		else: temp_times = None
		weekend_times = []
		# print(temp_times)
		if temp_times != None:
			for time_range in temp_times:
				if time_range[0] == 'Never':
					continue
				if time_range[0][-2:] == "PM":
					weekend_times.extend([int(time_range[0][:-2])+12,int(time_range[0][:-2])+1+12])
				else:
					weekend_times.extend([int(time_range[0][:-2]),int(time_range[0][:-2])+1])

		weekend_places_of_visit = []
		for i in df_req.iloc[0,11].split(";"):
			if building_name_to_id[i] == -1:
				continue
			weekend_places_of_visit.append(building_name_to_id[i])



		days = random.sample(['monday','tuesday','wednesday','thursday','friday'],no_of_weekdays)
		next_day = {'monday':'tuesday','tuesday':'wednesday','wednesday':'thursday','thursday':'friday','friday':'saturday'}
		list_places = {}
		m = 0
		for day in days:
			if len(places_of_visit) == 0:
				return
			if no_of_diff_places == 0:
				return
			list_places[day] = places_of_visit[m:m+no_of_diff_places]
			while len(list_places[day])<no_of_diff_places:
				list_places[day].extend(places_of_visit[0:no_of_diff_places-len(list_places[day])])
				m = -len(list_places[day])
				# print("hi", len(list_places[day]),no_of_diff_places)
			m+=no_of_diff_places
			if(m>no_of_diff_places):
				m = m % no_of_diff_places
		for day in days:
			last_class_time = 17
			while self.timetable[day][last_class_time] == self.timetable[day][18] and last_class_time > 14:
				last_class_time-=1
				# print("hi bye")
			outside_hours = random.sample(list(range(last_class_time+1,sleep_time)), min(len(range(last_class_time+1,sleep_time)),no_of_hours_weekdays))
			for hour in outside_hours:
				if hour <= 23:
					k={}
					for building in list_places[day]:
						k[building] = hall_wise_placeweights[str(self.residence_building_id)]['weekdays'][str(building)] + year_wise_placeweights[str(self.year)]['weekdays'][str(building)]
					self.timetable[day][hour] = k
				else:
					k={}
					for building in list_places[day]:
						k[building] = hall_wise_placeweights[str(self.residence_building_id)]['weekdays'][str(building)] + year_wise_placeweights[str(self.year)]['weekdays'][str(building)]
					self.timetable[next_day[day]][hour-24] = k

		#weekend movements
		for day in ['saturday','sunday']:
			for t in weekend_times:
				k={}
				for building in weekend_places_of_visit:
					k[building] = hall_wise_placeweights[str(self.residence_building_id)]['weekends'][str(building)] + year_wise_placeweights[str(self.year)]['weekends'][str(building)]
				self.timetable[day][t] = k










class professor(person):
	def __init__(self, prob_to_go_out=0.05, lab=None, office=None, Campus=None, HouseNo=None, ID=0, dept=None, inCampus=True, age=-1, ageclass=-1, role="faculty", year=None, schedule=None, master=None):
		super().__init__(ID=ID, role=role, age=age, ageclass=ageclass,dept=dept)
		self.personID = dept+str(ID)
		self.Campus = Campus
		self.residence = "Faculty Quarters"
		self.residence_building_id = [i for i in range(len(self.Campus.description)) if self.Campus.description[i]=='Faculty Residence'][0]
		self.residence_unit = Campus.Units_Placeholder[self.residence_building_id][HouseNo+self.Campus.Index_Holder[self.residence_building_id]]
		self.residence_point = self.residence_unit.location
		self.office = office
		self.prob_to_go_out = prob_to_go_out
		try:
			self.office_unit = self.Campus.__room2unit__(self.office)
			self.office_point = self.office_unit.location
		except:
			altroom = sum([ord(char) for char in office])+self.Campus.Index_Holder[42]
			self.office_unit = self.Campus.Units_Placeholder[42][altroom]
			self.office_point = self.office_unit.location
		self.lab = lab
		try:
			self.lab_unit = self.Campus.__room2unit__(self.lab)
			self.lab_point = self.lab_unit.location
		except:
			altroom = sum([ord(char) for char in office])+self.Campus.Index_Holder[42]
			self.lab_unit = self.Campus.Units_Placeholder[42][altroom]
			self.lab_point = self.lab_unit.location
		self.prof_timetable = schedule
		self.generate_exp_schedule()

	def generate_exp_schedule(self):
		for day in self.timetable:
				for i in range(24):
					if i < 8 or i >= 18 or i == 13:
						self.timetable[day][i] = self.residence_unit
						if i >= 18 and i <= 21:
							if random.random()<self.prob_to_go_out:
								building_id = random.choices(self.Campus.sectors['Market'].building_ids, weights=[95,5])[0] #Hard Coded 95 5 weights for market and rabi shop respectively
								unit_id = random.choice(list(self.Campus.sectors['Market'].Units_list[building_id].keys()))
								self.timetable[day][i] = self.Campus.sectors['Market'].Units_list[building_id][unit_id]
						#self.daily_schedule_expected[day][i] = 'residence'+str(self.residence_building_id)
					else:
						if day != 'sunday':
							self.timetable[day][i] = self.office_unit
							gaus_val = np.random.normal(0,1,1)
							if gaus_val >= -1 and gaus_val <=1: self.timetable[day][i] = self.lab_unit
							#self.daily_schedule_expected[day][i] = 'office'+self.office
						else:
							self.timetable[day][i] = self.residence_unit
							if random.random()<self.prob_to_go_out:
								building_id = random.choice(self.Campus.sectors['Market'].building_ids+self.Campus.sectors['Grounds'].building_ids+self.Campus.sectors['Restaurant'].building_ids) #TODO: have to send systematically on sundays; for now he has equal probabilty of going anywhere(i.e. all the mentioned sectors places)
								unit_id = random.choice(list(self.Campus.Units_Placeholder[building_id].keys()))
								self.timetable[day][i] = self.Campus.Units_Placeholder[building_id][unit_id]
							#self.daily_schedule_expected[day][i] = 'residence'+str(self.residence_building_id)

		day = {'0':'monday','1':'tuesday','2':'wednesday','3':'thursday','4':'friday','5':'saturday','6':'sunday'}
		class_start_time = {'0':'8','1':'9','2':'10','3':'11','4':'12','5':'14','6':'15','7':'16','8':'17'}
		try:
			for i in self.prof_timetable:
				for j in i[0]:
					self.prof_timetable[day[j[0]]][class_start_time[j[1]]] = i[1]
		except:
			# Enters this block when the schedule is given as a single subject
			for key, value in self.prof_timetable.items():
				for n in slots[value['slot']]:
					day = slots[value['slot']][n][0]
					times = map(int,slots[value['slot']][n][1].split('-'))
					for start_time in range(*times):
						try:
							#if day == 'wednesday':
							#    if value['room'][0:2] == 'NR' or value['room'][0:2] == 'NC':
							#        print(value['room'])
							#        print(start_time)
							self.timetable[day][start_time] = self.Campus.__room2unit__(value['room'])
							#self.daily_schedule_expected[day][start_time] = key
							#if day == 'wednesday': print(self.daily_schedule_expected['wednesday'])
						except:
							#print(value['room'])
							altroom = sum([ord(char) for char in value['room']])+self.Campus.Index_Holder[42]
							self.timetable[day][start_time]=self.Campus.Units_Placeholder[42][altroom]

class staff(person):
	def __init__(self,prob_to_go_out=0.1,HouseNo=None, workplace_buildingid = None,  Campus=None, ID=0,  inCampus=True, age=-1, ageclass=-1, role="staff", master=None):
		super().__init__(ID=ID, role=role, age=age, ageclass=ageclass)
		self.personID = 'St'+str(ID)
		self.Campus = Campus
		self.residence = "Staff Residence"
		self.residence_building_id = [i for i in range(len(self.Campus.description)) if self.Campus.description[i]=='Staff Residence'][0]
		self.residence_unit = Campus.Units_Placeholder[self.residence_building_id][HouseNo+self.Campus.Index_Holder[self.residence_building_id]]
		self.workplace_buildingid = workplace_buildingid
		self.prob_to_go_out = prob_to_go_out
		self.unit_ids_in_workplace_building = list(self.Campus.Units_Placeholder[self.workplace_buildingid].keys())
		self.generate_exp_schedule()

	def generate_exp_schedule(self):
		for day in self.timetable:
				for i in range(24):
					if i < 8 or i > 18 or i == 13:
						self.timetable[day][i] = self.residence_unit
						if i >= 18 and i <= 21:
							if random.random()<self.prob_to_go_out:
								building_id = random.choices(self.Campus.sectors['Market'].building_ids, weights=[95,5])[0] #Hard coded 95 for Tech Market 5 for Rabi Shop
								unit_id = random.choice(list(self.Campus.sectors['Market'].Units_list[building_id].keys()))
								self.timetable[day][i] = self.Campus.sectors['Market'].Units_list[building_id][unit_id]
					else:
						self.timetable[day][i] = self.workplace_unit = self.Campus.Units_Placeholder[self.workplace_buildingid][random.choice(self.unit_ids_in_workplace_building)]


'''
def main():
	from .utils import form_schedule
	from .campus import Sector, Unit
	from .parameters import Parameters, slots

	schedule = form_schedule()
	pm = Parameters('shapes/kgpbuildings.shp','Campus_data/KGP Data - Sheet1.csv')
	a = Sector(pm.returnParam())
	p = __init_students__(schedule,a)

	print(p[0].get_timetable())
	for i in range(len(p)):
		start_movement(p[i],p[i].get_timetable(),7)
	for key in p[0].schedule:
		print(time.strftime("%c",key),p[0].schedule[key])

if __name__ == "__main__":
	main()
'''
