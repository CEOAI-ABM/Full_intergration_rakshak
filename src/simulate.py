import random
import numpy as np
import time
from .utils import publish_loc, create_db_publish_locations
from .utils import get_movement_time_series

class Simulate():
    def __init__(self):
        self.SIMULATE   = True
        self.TODAY      = 1

        super().__init__()

    def simulation(self, all_persons, start_time=time.mktime(time.localtime()), no_of_days=30):
        self.start_time = start_time
        self.no_of_days = no_of_days
        self.all_persons = all_persons

        # Infect people intially

        # bookkeeping funks
        self.dbname, self.pswd = create_db_publish_locations()

        while (self.SIMULATE):
            self.__simulate_day__()
            if self.TODAY == self.no_of_days:
                self.SIMULATE = False

        
    def __save_results(self):
        # TODO: save case stats etc. + logging
        pass

    def __simulate_day__(self):
        # TODO (later): Lockdown checks go here
        # TODO (later): Travel to and from campus goes here 
        # TODO (later): CR and IFP Phases
        # TODO (later): Daily Transactions (TechM + Outside campus travel)

        # TODO (Vikram)
        # routine to update today's movements for all people into the mysql server
        # update should be in the correct format
        get_movement_time_series(self.all_persons, self.start_time)
        tmstamps = list(self.all_persons[0].today_schedule.keys())
        for tmstamp in tmstamps:
            if self.TODAY==1: temp = True
            else: temp = False
            publish_loc(self.all_persons,tmstamp,self.dbname,self.pswd,insert=temp)

        # TODO (Varun)
        # for healthy persons normal schedule
        # for hosp/quar etc policy will be diff
    
        # TODO (Varun)
        # routine to spread virus using contact graph

        # save case stats after today's spreading

        self.TODAY += 1
        pass
