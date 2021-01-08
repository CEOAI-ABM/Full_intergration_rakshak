import random
import ctypes
import numpy as np
import os
import random

from utils import form_schedule

# class person(ContactTracing, AgentStateA, TestingState):


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
    def __init__(self,pm=None,ID=0,dept=None,inCampus=True,age=-1,ageclass=-1,role="student",residence=None,year=None,schedule=None,master=None):
        super(person, self).__init__()

        self.ID         = ID
        self.pm         = pm
        self.Age        = age
        self.AgeClass   = ageclass
        self.master     = master

        # Whether the person is in 
        self.inCapmus   = inCampus

        self.residence = residence

        #  Namely student, faculty or staff
        self.Role = role

        if(self.Role=="student"):
            self.schedule = schedule
            self.dept = dept
        
        if(self.Role=="faculty"):
            self.dept = dept


def __init_students__(schedule):
    """ For initiating people & giving them their respective schedules

    Args: 
        schedule(dict): containing year-wise classes+labs with slots & rooms
    """
    depts   = ['AE', 'AG', 'AI', 'BT', 'CE', 'CH', 'CS', 'CY', 'EC', 'EE', 'EX', 'GG', 'HS', 'IE', 'IM', 'MA', 'ME', 'MF', 'MI', 'MT', 'NA', 'PH', 'QE', 'QM', 'RR']

    people = []

    ctr=1
    for dept in depts:
        dept_schedule = schedule[dept]
        for i in range(2,5):
            for j in range(1,random.randrange(40,60)):
                person_schedule = schedule[dept][i]
                age = str(18 + (i-1) + random.choice([0,1]))   
                junta = person(role="student",ID=ctr,age=age,year=j,schedule=person_schedule,dept=dept)
                people.append(junta)
    
    
                

def main():
    schedule = form_schedule()

    __init_students__(schedule)


if __name__ == "__main__":
    main()
