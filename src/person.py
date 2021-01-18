import random
import ctypes
import numpy as np
import os
import json
from sector import Sector, Unit
from param_with_shp import Parameters
from shapely.geometry import Point
import matplotlib.pyplot as plt

from utils import form_schedule

# class person(ContactTracing, AgentStateA, TestingState):
slots=json.load(open('Timetable/Schedule/slots.json'))

class person():
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

    def __init__(self,sectorptr=None,pm=None,ID=0,dept=None,inCampus=True,age=-1,ageclass=-1,role="student",year=None,schedule=None,master=None,residence='Hostel'):

        super(person, self).__init__()

        self.ID         = ID
        self.pm         = pm
        self.Age        = age
        self.AgeClass   = ageclass
        self.master     = master
        self.residence  = residence
        self.sector     = sectorptr
        if sectorptr!=None:
            self.residence_unit  = self.sector.Units_Placeholder[self.residence[0]][self.residence[1]+self.sector.Index_Holder[self.residence[0]]]

        # Whether the person is in 
        self.inCapmus   = inCampus
        self.timetable={"sunday":{},"monday":{}, "tuesday":{}, "wednesday":{}, "thursday":{}, "friday":{}, "saturday":{}}


        #  Namely student, faculty or staff
        self.Role = role

        if(self.Role=="student"):
            self.schedule = schedule
            self.dept = dept
        
        if(self.Role=="faculty"):
            self.dept = dept

    def get_timetable(self):
        for day in self.timetable:
            for i in range(24):
                self.timetable[day][str(i)+'-'+str(i+1)]=self.residence
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
                        self.timetable[times[0]][str(i)+'-'+str(i+1)]=class_room
                else:
                    self.timetable[times[0]][times[1]]=class_room
        return self.timetable

        


def __init_students__(schedule,sectorptr=None):
    """ For initiating people & giving them their respective schedules
    Args: 
        schedule(dict): containing year-wise classes+labs with slots & rooms
    """
    depts   = ['AE', 'AG', 'AI', 'BT', 'CE', 'CH', 'CS', 'CY', 'EC', 'EE', 'EX', 'GG', 'HS', 'IE', 'IM', 'MA', 'ME', 'MF', 'MI', 'MT', 'NA', 'PH', 'QE', 'QM', 'RR']

    people = []

    if sectorptr!=None:
        residence_indices = [i for i in range(len(sectorptr.ParamObj.description)) if sectorptr.ParamObj.description[i]=='Residence']
        weights = [sectorptr.Number_Units[i] for i in residence_indices]

    ctr=1
    for dept in depts:
        dept_schedule = schedule[dept]
        for i in range(2,5):
            for j in range(1,random.randrange(40,60)):
                person_schedule = schedule[dept][i]
                age = str(18 + (i-1) + random.choice([0,1]))
                if sectorptr!=None:
                    hall = random.choices(residence_indices,weights)[0]
                    room = random.randint(0,sectorptr.Number_Units[hall]-1)
                    junta = person(sectorptr=sectorptr,role="student",ID=ctr,age=age,year=j,schedule=person_schedule,dept=dept,residence=[hall,room])
                else:
                    junta = person(role="student",ID=ctr,age=age,year=j,schedule=person_schedule,dept=dept)
                people.append(junta)
    return people
    
    
                

def main():
    schedule = form_schedule()
    pm = Parameters('shapes/Untitled layer.shp','Campus_data/KGP Data - Sheet1.csv')
    a = Sector(pm.returnParam())
    p = __init_students__(schedule,a)
    print(p[0].get_timetable())
    plots = []
    for i in p:
        print(a.ParamObj.building_name[i.residence_unit.Building],i.residence_unit.location)

if __name__ == "__main__":
    main()
