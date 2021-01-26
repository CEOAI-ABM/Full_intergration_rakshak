import time
import json
from shapely.geometry import Point
from person import person
from sector import Sector
from param_with_shp import Parameters

class professor(person):
    def __init__(self,sectorptr=None,HouseNo=None,pm=None,ID=0,dept=None,inCampus=True,age=-1,ageclass=-1,role="faculty",year=None,schedule=None,master=None):
        super().__init__(ID=ID,role=role,age=age,dept=dept)
        self.sector = sectorptr
        self.residence = "Faculty Quarters"
        self.residence_building_id = [i for i in range(len(self.sector.ParamObj.description)) if self.sector.ParamObj.description[i]=='Faculty Residence'][0]
        self.residence_unit = sectorptr.Units_Placeholder[self.residence_building_id][HouseNo+self.sector.Index_Holder[self.residence_building_id]]
        self.pm = pm
        self.prof_timetable = schedule
        self.daily_schedule_expected = {"monday":{},"tuesday":{},"wednesday":{},"thursday":{},"friday":{},"saturday":{},"sunday":{}}
        generate_exp_schedule(self.prof_timetable,self.daily_schedule_expected)

def generate_exp_schedule(timetable,exp_sched):
    day = {'0':'monday','1':'tuesday','2':'wednesday','3':'thursday','4':'friday'}
    class_start_time = {'0':'8','1':'9','2':'10','3':'11','4':'12','5':'14','6':'15','7':'16','8':'17'}
    for i in timetable:
        for j in i[0]:
            exp_sched[day[j[0]]][time.strptime(day[j[0]]+' '+str(int(j[0])+1)+' '+class_start_time[j[1]],"%A %d %H")] = i[1]

def __init_profs__(schedule_data,sectorptr=None):
    people = []
    houseno = 0
    for i in schedule_data:
        people.append(professor(sectorptr=sectorptr,HouseNo=houseno,ID=houseno,dept=schedule_data[i]['dept'],schedule=schedule_data[i]['timetable']))
        houseno+=1
    return people


if __name__=='__main__':
    pm = Parameters('shapes/KgpBuildings.shp','Campus_data/KGP Data - Sheet1.csv')
    a = Sector(pm.returnParam())
    with open('TimeTable_Faculty/data.json') as fh:
        data = json.load(fh)
    p = __init_profs__(data,a)
    print(p[0].residence_unit)
    print(p[0].dept,p[0].daily_schedule_expected)
