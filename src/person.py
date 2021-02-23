import os
import json
import time
import ctypes
import random
import numpy as np
import geopandas as GP
import matplotlib.pyplot as plt
from shapely.geometry import Point
import matplotlib.animation as animation

from .parameters import slots
from .statemachine import AgentStatusA, AgentStateA, TestingState

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

    def __init__(self, Campus=None, ID=0, dept=None, inCampus=True, age=-1, ageclass=-1, role=None, year=None, schedule=None, master=None, residence=None):

        self.ID         = ID
        self.Age        = age
        self.AgeClass   = ageclass
        self.master     = master
        self.residence  = residence
        self.Campus     = Campus
        self.inCampus   = inCampus # Whether the person is currently in Campus
        self.Role = role #  Namely student, faculty or staff
        self.dept = dept

        self.timetable  = {"sunday": {}, "monday": {}, "tuesday": {}, "wednesday": {}, "thursday": {}, "friday": {}, "saturday": {}}

    def get_schedule(self):
        pass

# TODO: Make a separate student class that also inherits from person
class student(person):
    def __init__(self,  Campus=None, ID=0, dept=None, inCampus=True, age=-1, ageclass=-1, role="student", year=None, schedule=None, master=None,residence=None):
        super().__init__(ID=ID, role=role, age=age, dept=dept, residence=residence)
        self.Campus = Campus
        self.schedule = schedule
        self.residence_building_id = self.residence[0]
        self.residence_unit  = self.Campus.Units_Placeholder[self.residence[0]][self.residence[1]+self.Campus.Index_Holder[self.residence[0]]]
        self.residence_point = self.residence_unit.location
        self.get_timetable()

    def get_timetable(self):
        for day in self.timetable:
            for i in range(24):
                #self.timetable[day][str(i)+'-'+str(i+1)]=self.Campus.ParamObj.building_name[self.residence_unit.Building]
                self.timetable[day][i]=self.residence_unit
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
                            self.timetable[times[0]][i]=self.Campus.RoomNo_to_Unit(class_room)
                            self.Campus.RoomNo_to_Unit(class_room).isclassroom = True
                        except:
                            altroom = sum([ord(char) for char in class_room])+self.Campus.Index_Holder[42]
                            self.timetable[times[0]][i]=self.Campus.Units_Placeholder[42][altroom]
                            self.Campus.Units_Placeholder[42][altroom].isclassroom = True
                else:
                    self.timetable[times[0]][int(times[1].split('-')[0])]=self.Campus.RoomNo_to_Unit(class_room)
                    self.Campus.RoomNo_to_Unit(class_room).isclassroom = True

class professor(person):
    def __init__(self, lab=None, office=None, Campus=None, HouseNo=None, ID=0, dept=None, inCampus=True, age=-1, ageclass=-1, role="faculty", year=None, schedule=None, master=None):
        super().__init__(ID=ID, role=role, age=age, dept=dept)
        self.Campus = Campus
        self.residence = "Faculty Quarters"
        self.residence_building_id = [i for i in range(len(self.Campus.description)) if self.Campus.description[i]=='Faculty Residence'][0]
        self.residence_unit = Campus.Units_Placeholder[self.residence_building_id][HouseNo+self.Campus.Index_Holder[self.residence_building_id]]
        self.residence_point = self.residence_unit.location
        self.office = office
        try:
            self.office_unit = self.Campus.RoomNo_to_Unit(self.office)
            self.office_point = self.office_unit.location
        except:
            altroom = sum([ord(char) for char in office])+self.Campus.Index_Holder[42]
            self.office_unit = self.Campus.Units_Placeholder[42][altroom]
            self.office_point = self.office_unit.location
        self.lab = lab
        try:
            self.lab_unit = self.Campus.RoomNo_to_Unit(self.lab)
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
                    if i < 8 or i > 18 or i == 13:
                        self.timetable[day][i] = self.residence_unit
                        #self.daily_schedule_expected[day][i] = 'residence'+str(self.residence_building_id)
                    else:
                        if day != 'sunday':
                            self.timetable[day][i] = self.office_unit
                            gaus_val = np.random.normal(0,1,1)
                            if gaus_val >= -1 and gaus_val <=1: self.timetable[day][i] = self.lab_unit
                            #self.daily_schedule_expected[day][i] = 'office'+self.office
                        else:
                            self.timetable[day][i] = self.residence_unit
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
                            self.timetable[day][start_time] = self.Campus.RoomNo_to_Unit(value['room'])
                            #self.daily_schedule_expected[day][start_time] = key
                            #if day == 'wednesday': print(self.daily_schedule_expected['wednesday'])
                        except:
                            #print(value['room'])
                            altroom = sum([ord(char) for char in value['room']])+self.Campus.Index_Holder[42]
                            self.timetable[day][start_time]=self.Campus.Units_Placeholder[42][altroom]

def get_movement_time_series(persons, no_of_days):
    curr = time.localtime()
    day1 = time.mktime(time.struct_time((curr.tm_year,curr.tm_mon,curr.tm_mday,0,0,0,curr.tm_wday,curr.tm_yday,curr.tm_isdst)))
    for person in persons:
        tmstamp = day1
        newschedule = {}
        day = {0:'monday',1:'tuesday',2:'wednesday',3:'thursday',4:'friday',5:'saturday',6:'sunday'}
        for i in range(no_of_days):
            for j in range(24):
                try:
                    tp = person.timetable['monday'][0]
                    j1 = j
                except:
                    j1 = str(j)
                temp = tmstamp + j*60*60 + 24*60*60*i
                newschedule[time.localtime(temp)] = person.timetable[time.strftime("%A",time.localtime(temp)).casefold()][j1]
        person.schedule = newschedule

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
