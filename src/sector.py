import numpy as np
#from parm import Parameters
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
        Academic                    Pointer to the Academic class object calling it
    '''
    def __init__(self,Id,Building,Daily_People_Expectation,Number_Workers,Height,x_coordinate,y_coordinate,Sector):
        self.Id                         = Id
        self.Building                   = Building
        self.Sector                   = Sector
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
        0th pm is list of number of units of each academic 'Building'
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

        self.Index_Holder          = []
        self.Units_Placeholder          = {i:{} for i in range(self.Total_Num_Buildings)}

        self.People_In_Buildings        = [0]*(self.Total_Num_Buildings)
        #self.Number_Workplaces          = [0]*(self.Total_Num_Buildings)
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
    def __init__(self,pm):People_Expectation
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
        super()__init(pm)
        self.Types=['Indoor', 'Outdoor']
        self.Capacity={}


if __name__ == '__main__':
    pm = Parameters('Untitled layer.shp')
    #i = pm.BuildingInfo(BuildingName="Mechanical Engineering")['id']
    a = Sector(pm.returnParam())
    print("The Total Number of Buildings: ",a.Total_Num_Buildings)
