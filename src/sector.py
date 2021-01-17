import numpy as np
#from parm import Parameters
import shapes
from param_with_shp import Parameters
import matplotlib.pyplot as plt
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
    def __init__(self,Id,Building,Daily_People_Expectation,Number_Workers,Height,x_coordinate,y_coordinate,Sector):
        self.Id                         = Id
        self.Building                   = Building
        self.Sector                     = Sector
        self.Daily_People_Expectation   = Daily_People_Expectation
        self.Number_Workers             = Number_Workers
        self.height                     = Height
        self.x                          = x_coordinate
        self.y                          = y_coordinate
        self.working                    = []
        self.visiting                   = []


class Sector:
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
    def __init__(self,pm):
        self.Number_Units               = pm[0]
        self.Total_Num_Buildings        = len(self.Number_Units)
        self.Number_Workers             = pm[1]
        self.Height                     = pm[2]
        self.Location                   = [pm[3],pm[4]]
        self.Daily_People_Expectation   = pm[5]
        self.ParamObj                   = pm[6]

        self.Index_Holder               = []
        self.Units_Placeholder          = {i:{} for i in range(self.Total_Num_Buildings)}

        self.People_In_Buildings        = [0]*(self.Total_Num_Buildings)
        #self.Number_Workplaces         = [0]*(self.Total_Num_Buildings)
        self.initialize_units()

    def PeopleInAcademic(self):
        return sum(self.People_In_Buildings)

    def initialize_units(self):
        k = 0
        for building in range(self.Total_Num_Buildings):
            self.Index_Holder.append(k)
            #self.Number_Workplaces[building] = np.round(np.random.normal(np.array(self.Daily_People_Expectation[building]),np.array(self.Daily_People_Expectation[building])/6)).astype(np.int)

            if(self.Number_Units[building]>0):
                for j in range(self.Number_Units[building]):
                    self.Units_Placeholder[building][k]=Unit(j,building,self.Daily_People_Expectation[building][j],self.Number_Workers[building],self.Height[building][j],self.Location[0][building][j],self.Location[1][building][j],self)
                    k+=1


class Restaurant(Sector):
    def __init__(self,pm):
        super().__init__(pm[:-1])
        self.Types=['Dine In','Take Away']
        self.Capacity={}
        self.Factor=pm[-1]
        def update_capacity(self):
            for i in range(len(self.Number_Units)):
                self.Capacity[self.Types[i]]=self.Factor[i]*self.Sub_Class_People[i]

class Healthcare(Sector):
    def __init__(self,pm):
        super().__init__(pm[:-1])
        self.Types = ['Care_Center', 'Health_Center', 'Hospital']
        self.Capacity={}
        self.Factor=pm[-1]
        def update_capacity(self):
            for i in range(len(self.Number_Units)):
                self.Capacity[self.Types[i]]=self.Factor[i]*self.Sub_Class_People[i]

class Market(Sector):
    def __init__(self,pm):
        super().__init__(pm)
        self.Types=['Stationary', 'Vegetable Market', 'Department Store', 'Electronics Store']

class GymKhana(Sector):
    def __init__(self,pm):
        super().__init__(pm)
        self.Types=['Indoor', 'Outdoor']
        self.Capacity={}


if __name__ == '__main__':
    pm = Parameters('shapes/Untitled layer.shp','Campus_data/KGP Data - Sheet1.csv')
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
    p1 = plt.scatter([a.Units_Placeholder[31][k].x for k in a.Units_Placeholder[31]],[a.Units_Placeholder[31][k].y for k in a.Units_Placeholder[31]],marker='h')
    p2 = plt.scatter([a.Units_Placeholder[0][k].x for k in a.Units_Placeholder[0]],[a.Units_Placeholder[0][k].y for k in a.Units_Placeholder[0]],marker='.')
    p3 = plt.scatter([a.Units_Placeholder[2][k].x for k in a.Units_Placeholder[2]],[a.Units_Placeholder[2][k].y for k in a.Units_Placeholder[2]],marker='*')
    p4 = plt.scatter([a.Units_Placeholder[87][k].x for k in a.Units_Placeholder[87]],[a.Units_Placeholder[87][k].y for k in a.Units_Placeholder[87]],marker='s')
    p5 = plt.scatter([a.Units_Placeholder[8][k].x for k in a.Units_Placeholder[8]],[a.Units_Placeholder[8][k].y for k in a.Units_Placeholder[8]],marker='v')
    p6 = plt.scatter([a.Units_Placeholder[100][k].x for k in a.Units_Placeholder[100]],[a.Units_Placeholder[100][k].y for k in a.Units_Placeholder[100]],marker='x')
    p7 = plt.scatter([a.Units_Placeholder[32][k].x for k in a.Units_Placeholder[32]],[a.Units_Placeholder[32][k].y for k in a.Units_Placeholder[32]],marker="+")
    plt.axis('square')
    plt.show()

    #print("The Mechanical Engineering Building has rooms with following (ids,visitors) :",[(k,a.Units_Placeholder[i][k].visiting) for k in a.Units_Placeholder[i].keys()])
    #print(pm.BuildingInfo(BuildingName="Mechanical Engineering"))
    #print(a.Index_Holder)
