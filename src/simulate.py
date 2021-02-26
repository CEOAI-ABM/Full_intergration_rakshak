import random
import numpy as np
import time
import datetime
from .utils import publish_identity, publish_activity, create_db_publish_locations, get_movement_time_series
from .contact_graph import fullgraphplot

class Simulate():
    def __init__(self):
        self.SIMULATE   = True
        self.TODAY      = 1

        super().__init__()

    def simulation(self, start_time=None, no_of_days=30):
        self.start_time = start_time
        if start_time==None:
            curr = time.localtime()
            self.start_time = time.struct_time((curr.tm_year,curr.tm_mon,curr.tm_mday,0,0,0,curr.tm_wday,curr.tm_yday,curr.tm_isdst))
        self.no_of_days = no_of_days

        # Infect people intially

        # bookkeeping funks
        self.database_conn = create_db_publish_locations()
        publish_identity(self.all_people, self.database_conn, insert=True)
        self.curr_timestamp = time.localtime(time.mktime(self.start_time)+(self.TODAY-1)*24*60*60)

        while (self.SIMULATE):
            print("Simulating Day {}".format(self.TODAY))
            self.__simulate_day__()

            if self.TODAY > self.no_of_days:
                self.SIMULATE = False
        #fullgraphplot(datetime.datetime.fromtimestamp(time.mktime(self.start_time)),  datetime.datetime.fromtimestamp(time.mktime(self.start_time)+24*60*60))

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

        lockdown=False

        if len(self.SIsolatedP)+len(self.SHospitalizedP)+len(self.SIcuP) >=100:
            lockdown=True

        get_movement_time_series(self.all_people, self.curr_timestamp,lockdown)
        #print("get_movement_time_series done")
        tmstamps = list(self.all_people[0].today_schedule.keys())
        if self.TODAY==1: temp = True
        else: temp = False
        for tmstamp in tmstamps:
            #print(tmstamp)
            publish_activity(self.all_people, tmstamp, self.database_conn)
        #print("publish_activity done")

        # TODO 
        # for healthy persons normal schedule
        # for hosp/quar etc policy will be diff
        self.curr_timestamp = time.localtime(time.mktime(self.start_time)+(self.TODAY)*24*60*60)
        self.daily_transmissions()
        print('----------')
        print("Persons whose State is not Healthy")
        for s in self.all_people:
            if s.State != "Healthy":
                print("personid:", s.ID, "personState:",s.State, "personStatus", s.Status)
        print('----------')
        print()
        #print("student id = 1 contacts:")
        #self.__get_contacts__(self.Students[0])
        #print()
        #print("__get_contacts__ done")

        # TODO 
        # save case stats after today's spreading

        self.TODAY += 1
