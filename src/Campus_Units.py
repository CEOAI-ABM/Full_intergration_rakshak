import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point

class Unit():
    '''A Class for storing a unit of a Academic chain like a Nalanda classrooms, Department office etc.
        Takes 8 arguments:
        Id                          Id of place
        Building                    Building to which the unit belongs (Eg. Nalanda)
        Daily_People_Expectation    Daily expectation of people
        Number_Workers              Number of staff working here
        Height                      Floor
        x_coordinate                Location
        y_coordinate                Location
        Sector                    Pointer to the Sector class object calling it
    '''
    def __init__(self,Id,Building,Daily_People_Expectation,Number_Workers,Height,x_coordinate,y_coordinate,Sector,isclassroom=False):
        self.Id                         = Id
        self.Building                   = Building
        self.Sector                     = Sector
        self.Daily_People_Expectation   = Daily_People_Expectation
        self.Number_Workers             = Number_Workers
        self.height                     = Height
        self.location                   = Point(x_coordinate,y_coordinate)
        self.working                    = []
        self.visiting                   = []
        self.isclassroom                = isclassroom

# class Sector()

# class Academic

# TODO: All will inherit from sector
"""
class Restaurant():
    def __init__(self,pm):
        super().__init__(pm[:-1])
        self.Types=['Dine In','Take Away']
        self.Capacity={}
        self.Factor=pm[-1]
        def update_capacity(self):
            for i in range(len(self.Number_Units)):
                self.Capacity[self.Types[i]]=self.Factor[i]*self.Sub_Class_People[i]

class Healthcare():
    def __init__(self,pm):
        super().__init__(pm[:-1])
        self.Types = ['Care_Center', 'Health_Center', 'Hospital']
        self.Capacity={}
        self.Factor=pm[-1]
        def update_capacity(self):
            for i in range(len(self.Number_Units)):
                self.Capacity[self.Types[i]]=self.Factor[i]*self.Sub_Class_People[i]

class Market():
    def __init__(self,pm):
        super().__init__(pm)
        self.Types=['Stationary', 'Vegetable Market', 'Department Store', 'Electronics Store']

class GymKhana():
    def __init__(self,pm):
        super().__init__(pm)
        self.Types=['Indoor', 'Outdoor']
        self.Capacity={}

    '''Class for initializing the academic workplaces
        Takes list of parameters as argument:
        0th pm is list of number of units of each 'Building'
        1st pm is list of number of workers
        2nd pm is list of list of heights
        3rd pm is list of list of x-coordinates
        4th pm is list of list of y-coordinates
        5th pm is list of list of expected visitors coming in per day
        6th pm is the pointer to the parameters object itself
    '''
"""


if __name__ == '__main__':
    from parameters import Parameters
    pm = Parameters('shapes/kgpbuildings.shp','Campus_data/KGP Data - Sheet1.csv')
    #i = pm.BuildingInfo(BuildingName="Mechanical Engineering")['id']
    a = Sector(pm.returnParam())
    print("The Total Number of Buildings: ",a.Total_Num_Buildings)

    print(a.ParamObj.building_name[31])
    print(a.ParamObj.building_name[0])
    print(a.ParamObj.building_name[2])
    print(a.ParamObj.building_name[87])
    print(a.ParamObj.building_name[8])
    print(a.ParamObj.building_name[100])
    print(a.ParamObj.building_name[32])
   # p =[]
    #for i in range(len(a.Units_Placeholder)):
     #   p.append(plt.scatter([a.Units_Placeholder[i][k].x for k in a.Units_Placeholder[i]],[a.Units_Placeholder[i][k].y for k in a.Units_Placeholder[i]]))
    p1 = plt.scatter([a.Units_Placeholder[31][k].location.x for k in a.Units_Placeholder[31]],[a.Units_Placeholder[31][k].location.y for k in a.Units_Placeholder[31]],marker='h')
    p2 = plt.scatter([a.Units_Placeholder[0][k].location.x for k in a.Units_Placeholder[0]],[a.Units_Placeholder[0][k].location.y for k in a.Units_Placeholder[0]],marker='.')
    p3 = plt.scatter([a.Units_Placeholder[2][k].location.x for k in a.Units_Placeholder[2]],[a.Units_Placeholder[2][k].location.y for k in a.Units_Placeholder[2]],marker='*')
    p4 = plt.scatter([a.Units_Placeholder[87][k].location.x for k in a.Units_Placeholder[87]],[a.Units_Placeholder[87][k].location.y for k in a.Units_Placeholder[87]],marker='s')
    p5 = plt.scatter([a.Units_Placeholder[8][k].location.x for k in a.Units_Placeholder[8]],[a.Units_Placeholder[8][k].location.y for k in a.Units_Placeholder[8]],marker='v')
    p6 = plt.scatter([a.Units_Placeholder[100][k].location.x for k in a.Units_Placeholder[100]],[a.Units_Placeholder[100][k].location.y for k in a.Units_Placeholder[100]],marker='x')
    p7 = plt.scatter([a.Units_Placeholder[32][k].location.x for k in a.Units_Placeholder[32]],[a.Units_Placeholder[32][k].location.y for k in a.Units_Placeholder[32]],marker="+")
    plt.axis('square')
    plt.show()

    #print("The Mechanical Engineering Building has rooms with following (ids,visitors) :",[(k,a.Units_Placeholder[i][k].visiting) for k in a.Units_Placeholder[i].keys()])
    #print(pm.BuildingInfo(BuildingName="Mechanical Engineering"))
    #print(a.Index_Holder)
