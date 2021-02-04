import time
import json
from shapely.geometry import Point
from person import person
from sector import Sector
from param_with_shp import Parameters
from utils import form_schedule
import matplotlib.pyplot as plt
import matplotlib.animation as animation

slots=json.load(open('Timetable/Schedule/slots.json'))

class professor(person):
    def __init__(self,lab=None,office=None,sectorptr=None,HouseNo=None,pm=None,ID=0,dept=None,inCampus=True,age=-1,ageclass=-1,role="faculty",year=None,schedule=None,master=None):
        super().__init__(ID=ID,role=role,age=age,dept=dept)
        self.sector = sectorptr
        self.residence = "Faculty Quarters"
        self.residence_building_id = [i for i in range(len(self.sector.ParamObj.description)) if self.sector.ParamObj.description[i]=='Faculty Residence'][0]
        self.residence_unit = sectorptr.Units_Placeholder[self.residence_building_id][HouseNo+self.sector.Index_Holder[self.residence_building_id]]
        self.residence_point = self.residence_unit.location
        self.office = office
        try:
            self.office_unit = self.sector.RoomNo_to_Unit(self.office)
            self.office_point = self.office_unit.location
        except:
            pass
        self.lab = lab
        try:
            self.lab_unit = self.sector.RoomNo_to_Unit(self.lab)
            self.lab_point = self.lab_unit.location
        except:
            pass
        self.pm = pm
        self.prof_timetable = schedule
        self.daily_schedule_expected = {"monday":{},"tuesday":{},"wednesday":{},"thursday":{},"friday":{},"saturday":{},"sunday":{}}
        self.generate_exp_schedule()

    def generate_exp_schedule(self):
        for day in self.daily_schedule_expected:
                for i in range(24):
                    if i < 8 and i > 6:
                        self.daily_schedule_expected[day][str(i)] = self.residence_point
                    else:
                        self.daily_schedule_expected[day][str(i)] = self.office_point

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
                        self.daily_schedule_expected[day][start_time] = self.sector.RoomNo_to_Unit(value['room']).location

def __init_profs__(schedule_data,sectorptr=None):
    people = []
    houseno = 0
    for i in schedule_data:
        people.append(professor(sectorptr=sectorptr,HouseNo=houseno,ID=houseno,dept=schedule_data[i]['dept'],schedule=schedule_data[i]['timetable']))
        houseno+=1
    return people

def init_profs_from_schedule(schedule,sectorptr):
    '''Takes the dict returned by form_schedule
        Assigns 1 prof 1 course
    '''
    people = []
    houseno = 0
    for i in schedule:
        dept_roomno = 0
        for j in schedule[i]:
            for k in schedule[i][j]:
                subj = {k: schedule[i][j][k]}
                dept = i
                lab = dept+str(dept_roomno)
                office_no = (len([d for d in sectorptr.Rooms if d[0:2]==dept])-dept_roomno-1)
                office=dept+str(office_no)
                someno = office_no
                while someno>0 and sectorptr.RoomNo_to_Unit(office).isclassroom == True:
                    someno-=1
                    office=dept+str(someno)
                else:
                    if someno < 0:
                        office = lab
                people.append(professor(sectorptr=sectorptr,HouseNo=houseno,ID=houseno,dept=dept,schedule=subj,lab=lab,office=office))
                houseno+=1
                dept_roomno+=1
    return people



if __name__=='__main__':
    pm = Parameters('shapes/KgpBuildings.shp','Campus_data/KGP Data - Sheet1.csv')
    a = Sector(pm.returnParam())
#    with open('TimeTable_Faculty/data.json') as fh:
#        data = json.load(fh)
#    p = __init_profs__(data,a)
    schedule = form_schedule()
    p = init_profs_from_schedule(schedule,a)
    print(p[0].residence_unit)
    print(p[0].dept,p[0].daily_schedule_expected)

    pa=[]
    pb=[]
    #print(p[0].get_timetable())
    for t in range(len(p)):
        pointa = []
        pointb = []
        for key,value in p[t].daily_schedule_expected.items():
            for aa,b in value.items():
                pointa.append(b.x)
                pointb.append(b.y)
        pa.append(pointa)
        pb.append(pointb)

    print(pointa,pointb)
    fig = plt.figure()
    for i in a.ParamObj.polygons:
        plt.plot(*i.exterior.xy)
    ax = plt.axes(xlim=(-300, 0), ylim=(0,300))
    x, y = [[],[]]
    mat, = ax.plot(x, y, 'o')


    def init():
        mat.set_data([],[])
        for i in a.ParamObj.polygons:
            plt.plot(*i.exterior.xy)

    # animation function.  This is called sequentially
    def animate(i):
        x = [pa[k][i] for k in range(len(p))]
        y = [pb[k][i] for k in range(len(p))]
        mat.set_data(x,y)
        return mat,

    anim = animation.FuncAnimation(fig, animate, interval=200)

    plt.show()
