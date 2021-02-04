import numpy as np
from param_with_shp import Parameters
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
        self.RoomCodes                  = []
        self.Rooms                      = {}
        self.Index_Holder               = []
        self.Units_Placeholder          = {i:{} for i in range(self.Total_Num_Buildings)}

        self.People_In_Buildings        = [0]*(self.Total_Num_Buildings)
        #self.Number_Workplaces         = [0]*(self.Total_Num_Buildings)
        self.initialize_units()

    def RoomNo_to_Unit(self,room_name):
        if room_name[0] == 'V':
            code = room_name[0]
            number = room_name[1:]
        else:
            code = room_name[0:2]
            if code == 'NC':
                allrooms=['NC131', 'NC132', 'NC141', 'NC142', 'NC231', 'NC232', 'NC233', 'NC234', 'NC241', 'NC242', 'NC243', 'NC244', 'NC331', 'NC332', 'NC333', 'NC334', 'NC341', 'NC342', 'NC343', 'NC344', 'NC431', 'NC432', 'NC433', 'NC434', 'NC441', 'NC442', 'NC443', 'NC444']
                number = str(allrooms.index(room_name))
            elif code == 'NR':
                allrooms=['NR121', 'NR122', 'NR123', 'NR124', 'NR221', 'NR222', 'NR223', 'NR224', 'NR321', 'NR322', 'NR323', 'NR324', 'NR421', 'NR422', 'NR423', 'NR424']
                number = str(allrooms.index(room_name))
            elif code == 'S-':
                allrooms = ['S-123', 'S-125', 'S-126', 'S-127', 'S-136', 'S-216', 'S-122A', 'S-301', 'S-302']
                number = str(allrooms.index(room_name))
            elif len(room_name) == 5 and room_name[3]=='L':
                number = str(int(room_name[2]+room_name[4])-20)
            else:
                number = room_name[2:]
                #print(code+number)
        return self.Rooms[code+number]

    def initialize_units(self):
        k = 0
        for building in range(self.Total_Num_Buildings):
            self.Index_Holder.append(k)
            #self.Number_Workplaces[building] = np.round(np.random.normal(np.array(self.Daily_People_Expectation[building]),np.array(self.Daily_People_Expectation[building])/6)).astype(np.int)

            if(self.Number_Units[building]>0):
                temp_room_code = self.ParamObj.df['Abbreviation'][building]
                if type(temp_room_code) != type(0.1):
                    self.RoomCodes.append(temp_room_code.split(','))
                    #print(self.RoomCodes[-1])
                for j in range(len(self.Height[building])):
                    #print(len(self.Location[0][building]),j,self.Height[building])
                    self.Units_Placeholder[building][k]=Unit(j,building,self.Daily_People_Expectation[building][j],self.Number_Workers[building],self.Height[building][j],self.Location[0][building][j],self.Location[1][building][j],self)
                    if type(temp_room_code) != type(0.1):
                        some_temp_no = int(j/(len(self.Height[building])//len(self.RoomCodes[-1])))
                        if some_temp_no >= len(self.RoomCodes[-1]): some_temp_no = len(self.RoomCodes[-1])-1
                        roomcode = self.RoomCodes[-1][some_temp_no]
                        self.Rooms[roomcode+str(j-((len(self.Height[building])//len(self.RoomCodes[-1])))*some_temp_no)]=self.Units_Placeholder[building][k]
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
    pm = Parameters('shapes/KgpBuildings.shp','Campus_data/KGP Data - Sheet1.csv')
    #i = pm.BuildingInfo(BuildingName="Mechanical Engineering")['id']
    a = Sector(pm.returnParam())
    print("The Total Number of Buildings: ",a.Total_Num_Buildings)
    #print([d for d in a.Rooms if d[0:2]=='NA'])
    print(a.Rooms['NA0'])

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
