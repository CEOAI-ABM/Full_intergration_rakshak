import time
from shapely.geometry import Point
from .person import person

class professor(person):
    def __init__(self,pm=None,ID=0,dept=None,inCampus=True,age=-1,ageclass=-1,role="faculty",residence=None,year=None,schedule=None,master=None):
        super().__init__(ID=ID,role=role,age=age,residence=residence,dept=dept)
        self.pm = pm
        self.office = self.pm.office
        self.lab  = self.pm.lab
