import numpy as np

class Academic_Unit():
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
    def __init__(self,Id,Building,Daily_People_Expectation,Number_Workers,Height,x_coordinate,y_coordinate,Academic):
        self.Id                         = Id
        self.Building                   = Building
        self.Academic                   = Academic
        self.Daily_People_Expectation   = Daily_People_Expectation
        self.Number_Workers             = Number_Workers
        self.height                     = Height
        self.x                          = x_coordinate
        self.y                          = y_coordinate
        self.working                    = []
        self.visiting                   = []


class Academic:
    '''Class for initializing the academic workplaces
        Takes list of parameters as argument:
        0th pm is list of number of units of each academic 'Building'
        1st pm is list of number of workers
        2nd pm is list of heights
        3rd pm is list of x-coordinates
        4th pm is list of y-coordinates
        5th pm is list of expected visitors coming in per day
    '''
    def __init__(self,pm):
        self.Number_Units               = pm[0]
        self.Total_Num_Buildings        = len(self.Number_Units)
        self.Number_Workers             = pm[1]
        self.Height                     = pm[2]
        self.Location                   = [pm[3],pm[4]]
        self.Daily_People_Expectation   = pm[5]

        self.Index_Holder          = []
        self.Units_Placeholder          = {i:[] for i in range(self.Total_Num_Buildings)}

        self.People_In_Buildings        = [0]*(self.Total_Num_Buildings)
        self.Number_Workplaces          = [0]*(self.Total_Num_Buildings)
        self.initialize_units()

    def PeopleInAcademic(self):
        return sum(self.People_In_Buildings)

    def initialize_units(self):
        k = 0
        self.Index_Holder.append(k)
        for building in range(self.Total_Num_Buildings):
            #self.Number_Workplaces[building] = np.round(np.random.normal(self.Daily_People_Expectation[building],self.Daily_People_Expectation[building]/6)).astype(np.int)
            #self.Units_Placeholder[k] = []
            if(self.Number_Units[building]>0):
                for j in range(self.Number_Units[building]):
                    self.Units_Placeholder[k].append(Academic_Unit(j,building,self.Daily_People_Expectation[building][j],self.Number_Workers[building],self.Height[building][j],self.Location[0][building][j],self.Location[1][building][j],self))
            k+=1

#if __name__ == '__main__':
#    a = Academic([[2,2,1],[20,10,5],[[1,2],[3,4],[5]],[[1,2],[3,4],[5]],[[1,2],[3,4],[5]],[[10,20],[30,40],[5]]])
#    print(a.Daily_People_Expectation)
#    print(a.Units_Placeholder)
import numpy as np

class Residence_Unit:
    """A Class for storing a unit of a Residence i.e., a room of a hostel or a house or mess
        Takes 5 parameters
        Id no. for an residence i.e., each residence is given a Id No.
        Room No. of place
        Height and Location
    """
    def __init__(self,Id,Building,Daily_People_Expectation,Number_Workers,Height,x_coordinate,y_coordinate,Inter_Person_Distance):

        self.Id                         = Id
        self.Building                   = Building
        self.Residence                  = Residence
        self.Daily_People_Expectation   = Daily_People_Expectation
        self.Number_Workers             = Number_Workers
        self.height                     = Height
        self.x                          = x_coordinate
        self.y                          = y_coordinate
        self.Inter_Person_Distance      = Inter_Person_Distance
        self.working                    = []
        self.visiting                   = []

class Residence:
    """Class for storing
    Args:
        0th pm is number of rooms
        1st pm is the number of workers
        2nd pm is the x-coordinates
        3rd pm is the y-coordinates
        4th pm the heights
        5th pm the hostel name
    """
    def __init__(self,pm):

        self.Number_Rooms               = pm[0]
        self.Total_Num_Buildings        = len(self.Number_Rooms)
        self.Number_Workers             = pm[1]
        self.height                     = pm[2]
        self.Location                   = [pm[3],pm[4]]
        self.Daily_People_Expectation   = pm[5]
        self.Name                       = pm[6]
        self.Inter_Person_Distance      = pm[7]

        self.Units_Placeholder={}


    def initialize_units(self):
        for i in range(len(self.Number_Rooms)):
            if(self.Number_Rooms[i]>0):
                self.Units_Placeholder[Name[i]]=[];
                for j in range(self.Number_Rooms[i]):
                    self.Units_Placeholder[].append(Residence_Unit(j,i,self.Daily_People_Expectation[i][j],self.Number_Workers[i][j],self.Height[i][j],self.Location[0][i][j],self.Location[1][i][j],self.Inter_Person_Distance[i][j]))
