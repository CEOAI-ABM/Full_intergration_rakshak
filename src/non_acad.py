class Unit(object):
    """A Class for storing a unit of a Type of Non Academic chain like a Restaurant
        Takes 8 parameters
        Id of place
        Class of the Unit
        Daily expectation of people
        Number of workers working here
        Height of the place
        X-coordinate of the place
        Y-Coordinate of the place
        Inter Person Distance
    """
    def __init_(self,id,Class,Daily_People_Expectation,Number_Workers,Height,X_coordinate,Y_coordinate, Inter_Person_Distance):
        super(Non_Academic,self).__init__()
        self.Id=id
        self.Class=Class
        self.Daily_People_Expectation=Daily_People_Expectation
        self.Number_Workers=Number_Workers
        self.height=height
        self.x=X_coordinate
        self.y=Y_coordinate
        self.inter_person_distance=Inter_Person_Distance
        self.working=[]
        self.visiting=[]

class Non_Academic():
    """Class for storing

    Args:
        0th pm is number of units of this commercial body
        1st pm is the number of workers
        2nd pm is the x-coordinates
        3rd pm is the y-coordinates
        4th pm the heights
        5th pm is the expected customers coming in per day
        6th parameter is the interperson distance
    """

    def __init__(self,pm):
        super(Non_Academic,self).__init__()
        self.Number_Units=pm[0]
        self.Number_of_Types=len(self.Number_Units)
        self.Number_Workers=pm[1]
        self.Location=[pm[2],pm[3]]
        self.Height=pm[4]
        self.Daily_People_Expectation=pm[5]
        self.Inter_Person_Distance=pm[6]

        # self.Index_Holder=[]
        self.Units_Placeholder = {i:[] for i in range(self.Number_of_Types)}

        # self.People_In_Units=0
        # self.Sub_Class_People=[0]*(len(self.Number_Units))
        # self.Number_Incapacitated=0

        self.initialize_units()
    
    def initialize_units(self):
        k=0
        # self.Index_Holder.append(k)

        for i in range(self.Number_of_Typese):
            if(self.Number_Units[i]>0):
                for j in range(self.Number_Units[i]):
                    self.Units_Placeholder[k].append(Unit(j,i,self.Daily_People_Expectation[i],self.Number_Workers[i],self.Height[i][j],self.Location[0][i][j],self.Location[1][i][j], self.Inter_Person_Distance[i][j]))
                   # self.Index_Holder.append(k)
            k+=1
            # self.Index_Holder.append(k)

class Restaurant(Non_Academic):
    def __init__(self,pm):People_Expectation
        super().__init__(pm[0])
        self.Types=['Dine In','Take Away']
        self.Capacity={}
        self.Factor=pm[1]
        def update_capacity(self):
            for i in range(len(self.Number_Units)):
                self.Capacity[self.Types[i]]=self.Factor[i]*self.Sub_Class_People[i]

class Healthcare(Non_Academic):
    def __init__(self,pm):
        super().__init__(pm[0])
        self.Types = ['Care_Center', 'Health_Center', 'Hospital']
        self.Capacity={}
        self.Factor=pm[1]
        def update_capacity(self):
            for i in range(len(self.Number_Units)):
                self.Capacity[self.Types[i]]=self.Factor[i]*self.Sub_Class_People[i]

class Market(Non_Academic):
    def __init__(self,pm):
        super().__init__(pm)
        self.Types=['Stationary', 'Vegetable Market', 'Department Store', 'Electronics Store']

class GymKhana(Non_Academic):
    def __init__(self,pm):
        super()__init(pm)
        self.Types=['Indoor', 'Outdoor']
        self.Capacity={}








        



