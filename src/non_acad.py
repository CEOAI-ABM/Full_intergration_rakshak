class Unit(object):
    """A Class for storing a unit of a Non Academic chain like a restaurant
        Takes 7 parameters
        Id of place
        Class of the Unit
        Daily expectation of people
        Number of workers working here
        Height of the place
        X-coordinate of the place
        Y-Coordinate of the place
    """
    def __init_(self,id,Class,Daily_People_Expectation,Number_Workers,Height,x_coordinate,y_coordinate):
        super(Non_Academic,self).__init__()
        self.Id=id
        self.Class=Class
        self.Daily_People_Expectation=Daily_People_Expectation
        self.Number_Workers=Number_Workers
        self.height=height
        self.x=x_coordinate
        self.y=y_coordinate
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
    """
    def __init__(self,pm):
        super(Non_Academic,self).__init__()
        self.Number_Units=pm[0]
        self.Number_Workers=pm[1]
        self.Location=(pm[2],pm[3])
        self.Height=pm[4]
        self.Daily_People_Expectation=pm[5]

        self.Index_Holder=[]
        self.Units_Placeholder=[]

        self.People_In_Units=0
        self.Sub_Class_People=[0]*(len(self.Number_Units))
        self.Number_Incapacitated=0
    
    def initialize_units(self):
        k=0
        self.Index_Holder.append(k)

        for i in range(len(self.Total_Different_Non_Academic_Blocks)):
            if(self.Number_Units[i]>0):
                for j in range(self.Number_Units[i]):
                    self.Units_Placeholder.append(Unit(j,i,self.Daily_People_Expectation[i],self.Number_Workers[i],self.Height[i][j],self.Location[0][i][j],self.Location[1][i][j]))
                    k+=1
            self.Index_Holder.append(k)

class Restaurant(Non_Academic):
    def __init__(self,pm):
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






        



