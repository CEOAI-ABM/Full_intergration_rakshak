import random
import ctypes
import numpy as np
import os
import json
from sector import Sector, Unit
from param_with_shp import Parameters
from shapely.geometry import Point
import matplotlib.pyplot as plt
import geopandas as GP
import matplotlib.animation as animation
import time

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
                #self.timetable[day][str(i)+'-'+str(i+1)]=self.sector.ParamObj.building_name[self.residence_unit.Building]
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
                            self.timetable[times[0]][i]=self.sector.RoomNo_to_Unit(class_room)
                            self.sector.RoomNo_to_Unit(class_room).isclassroom = True
                        except:
                            altroom = sum([ord(char) for char in class_room])+self.sector.Index_Holder[42]
                            self.timetable[times[0]][i]=self.sector.Units_Placeholder[42][altroom]
                            self.sector.Units_Placeholder[42][altroom].isclassroom = True
                else:
                    self.timetable[times[0]][int(times[1].split('-')[0])]=self.sector.RoomNo_to_Unit(class_room)
                    self.sector.RoomNo_to_Unit(class_room).isclassroom = True
        return self.timetable

    def get_schedule(self):
        pass

def start_movement(person,schedule,no_of_days):
    curr = time.localtime()
    day1 = time.mktime(time.struct_time((curr.tm_year,curr.tm_mon,curr.tm_mday,0,0,0,curr.tm_wday,curr.tm_yday,curr.tm_isdst)))
    tmstamp = day1
    newschedule = {}
    day = {0:'monday',1:'tuesday',2:'wednesday',3:'thursday',4:'friday',5:'saturday',6:'sunday'}
    for i in range(no_of_days):
        for j in range(24):
            try:
                tp = schedule['monday'][0]
                j1 = j
            except:
                j1 = str(j)
            temp = tmstamp + j*60*60 + 24*60*60*i
            newschedule[time.localtime(temp)] = schedule[time.strftime("%A",time.localtime(temp)).casefold()][j1]
    person.schedule = newschedule


def __init_students__(schedule,sectorptr=None):
    """ For initiating people & giving them their respective schedules
    Args:
        schedule(dict): containing year-wise classes+labs with slots & rooms
    """
    depts   = ['AE', 'AG', 'AR', 'BT', 'CE', 'CH', 'CS', 'CY', 'EC', 'EE', 'EX', 'GG', 'HS', 'IE', 'IM', 'MA', 'ME', 'MF', 'MI', 'MT', 'NA', 'PH', 'QE', 'QM']

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
                    room = random.randint(0,len(sectorptr.Height[hall])-1)
                    junta = person(sectorptr=sectorptr,role="student",ID=ctr,age=age,year=j,schedule=person_schedule,dept=dept,residence=[hall,room])
                    ctr += 1
                else:
                    junta = person(role="student",ID=ctr,age=age,year=j,schedule=person_schedule,dept=dept)
                people.append(junta)
    return people




def main():
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
