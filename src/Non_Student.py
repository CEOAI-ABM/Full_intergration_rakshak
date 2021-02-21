import time
import json
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point
import matplotlib.animation as animation

from .person import person
from .parameters import slots
from .utils import form_schedule

class non_acad_staff(person):
    print(12)
    pass

"""
def __init_profs__(schedule_data,sectorptr=None):
    people = []
    houseno = 0
    for i in schedule_data:
        people.append(professor(sectorptr=sectorptr,HouseNo=houseno,ID=houseno,dept=schedule_data[i]['dept'],schedule=schedule_data[i]['timetable']))
        houseno+=1
    return people
"""

if __name__=='__main__':
    from campus import Sector 
    from parameters import Parameters, slots
    from person import start_movement

    pm = Parameters('shapes/kgpbuildings.shp','Campus_data/KGP Data - Sheet1.csv')
    a = Sector(pm.returnParam())
#    with open('TimeTable_Faculty/data.json') as fh:
#        data = json.load(fh)
#    p = __init_profs__(data,a)
    schedule = form_schedule()
    p = init_profs_from_schedule(schedule,a,1)
    print(p[0].residence_point)
    print(p[0].dept,p[0].daily_schedule_expected)
    #print(p[0].Role,p[0].schedule)
    for k in range(len(p)):
        start_movement(p[k], p[k].daily_schedule_expected, no_of_days=7)
    for key in p[0].schedule:
        print(time.strftime("%c",key),p[0].schedule[key])


