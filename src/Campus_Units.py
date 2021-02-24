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
    def __init__(self,Id,Building,Daily_People_Expectation,Number_Workers,Height,x_coordinate,y_coordinate,Sector,area,isclassroom=False):
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
        self.area                       = area
        self.interpersonDist            = None  #function(self.area,self.working+self.visiting)

class Sector():

    def __init__(self,pm,SectorName):
        self.building_ids               = []
        self.SectorName                 = SectorName
        self.num_rooms_per_floor        = {}
        self.Daily_People_Expectation   = {}
        self.Number_Workers             = {}
        self.height                     = {}
        self.location                   = {}
        self.building_area              = {}
        self.Units_list                 = {}
        self.rooms_packing_fraction     = {} # denotes how much of the area of a floor is covered by all the rooms
        self.room_area                  = {}

        self.__get_building_ids__(pm)

        self.Number_Buildings                   = len(self.building_ids)

        for i in self.building_ids:
            self.Units_list[i]                  = {}
            self.num_rooms_per_floor[i]         = pm.num_rooms_per_floor[i]
            self.Daily_People_Expectation[i]    = pm.Daily_People_Expectation[i]
            self.Number_Workers[i]              = pm.Number_Workers[i]
            self.height[i]                      = pm.heights[i]
            self.location[i]                    = [pm.xlist[i], pm.ylist[i]]
            self.building_area[i]               = pm.polygons[i].area
            self.rooms_packing_fraction[i]      = pm.rooms_packing_fraction[i]
            self.room_area[i]                   = self.rooms_packing_fraction[i]*self.building_area[i]/self.num_rooms_per_floor[i]


    def __get_building_ids__(self, pm):
        i = 0
        while i < len(pm.description):
            if pm.description[i] in self.SectorName:
                self.building_ids.append(i)
            i+=1

class Academic(Sector):
    def __init__(self,pm):
        super().__init__(pm, ['Academic'])
        self.Types              = ['Classroom', 'Office']

class Residence(Sector):
    def __init__(self,pm):
        super().__init__(pm, ['Residence', 'Faculty Residence', 'Staff Residence'])
        self.Types              = ['Student Residence', 'Faculty Residence', 'Guest House', 'Staff Residence']

# TO DO: All will inherit from sector

class Restaurant(Sector):
    def __init__(self,pm, Factor=None):
        super().__init__(pm, ['Restaurant'])
        self.Types              = ['Dine In','Take Away']
        self.Capacity           = {}
        self.Factor             = Factor

        def update_capacity(self):
            for i in range(len(self.num_rooms_per_floor)):
                self.Capacity[self.Types[i]]=self.Factor[i]*self.Sub_Class_People[i]

class Healthcare(Sector):
    def __init__(self, pm, Factor=None):
        super().__init__(pm, ['Healthcare'])
        self.Types              = ['Care_Center', 'Health_Center', 'Hospital']
        self.Capacity           = {}
        self.Factor             = Factor

        def update_capacity(self):
            for i in range(len(self.num_rooms_per_floor)):
                self.Capacity[self.Types[i]]=self.Factor[i]*self.Sub_Class_People[i]

class Market(Sector):
    def __init__(self,pm):
        super().__init__(pm, ['Market'])
        self.Types              = ['Stationary', 'Vegetable Market', 'Department Store', 'Electronics Store']

class Gymkhana(Sector):
    def __init__(self,pm):
        super().__init__(pm, ['Gymkhana'])
        self.Types              = ['Indoor', 'Outdoor']
        self.Capacity={}

class Grounds(Sector):
    def __init__(self,pm):
        super().__init__(pm, ['Grounds'])
        self.Types              = ['Sports', 'Parks']

class Non_Academic(Sector):
    def __init__(self,pm):
        super().__init__(pm, ['Non_Academic'])

class Guest_House(Sector):
    def __init__(self,pm):
        super().__init__(pm, ['Guest House'])
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
