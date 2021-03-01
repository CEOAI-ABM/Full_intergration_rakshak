import time
import random
import datetime
import numpy as np

from .mysql_utils import publish_identity, publish_activity, create_db_publish_locations

class Simulate():
    def __init__(self):
        self.SIMULATE   = True
        self.TODAY      = 1

        super().__init__()

    def __init_infected__(self, num=1):
        """
        Infect people initially as required
        """
        persons_to_infect = random.sample(self.all_people, num)
        
        for person in persons_to_infect:
            print('Infected person {} who is a {} initially'.format(person.ID, person.Role))
            self.__infect_person__(person)
    
    def simulation(self, start_time=None):
        """
        Main function to set up the simulation, simulate each day and save the results
        """

        # Set sim start day
        self.start_time = start_time
        if start_time==None:
            curr = time.localtime()
            self.start_time = time.struct_time((curr.tm_year,curr.tm_mon,curr.tm_mday,0,0,0,curr.tm_wday,curr.tm_yday,curr.tm_isdst))

        # Infect people initially
        self.__init_infected__(num=2)

        # Establish database connection
        self.db_conn = create_db_publish_locations()
        #publish_identity(self.all_people, self.db_conn)
        self.curr_timestamp = time.localtime(time.mktime(self.start_time)+(self.TODAY-1)*24*60*60)
        # Simulation loop
        while (self.SIMULATE):
            print("Simulating Day {}".format(self.TODAY))
            
            self.__simulate_day__()

            #if self.TODAY%self.pm.duration == 0:
                #TODO: clear activity table
            #    pass

            if self.TODAY > self.SIM_DAYS:
                self.SIMULATE = False

    def __simulate_day__(self):
        """
        Simulate one day
        """
        # TODO (later): Lockdown checks go here
        # TODO (later): Travel to and from campus goes here
        # TODO (later): CR and IFP Phases
        # TODO (later): Daily Transactions (TechM + Outside campus travel)

        self.__update_movement_time_series__(self.all_people, self.curr_timestamp)
        self.__update_today_movements__() 
        self.curr_timestamp = time.localtime(time.mktime(self.start_time)+(self.TODAY)*24*60*60)
        # Spreading of virus
        self.daily_transmissions()

        # TODO: Save case stats after today's spreading
        self.__save_results__()

        self.TODAY += 1

    def __save_results__(self):
        # TODO: save case stats etc. to file instead of printing 
        print('----------')
        print("Persons whose State is not Healthy")
        for s in self.all_people:
            if s.State != "Healthy":
                print("personid:", s.ID, "personState:", s.State, "personStatus", s.Status)
        print('----------')
        print()

    def __update_today_movements__(self):
        """
        Publish today's movements in the MySQL server
        """
        tmstamps = list(self.all_people[0].today_schedule.keys())
        for tmstamp in tmstamps:
            publish_activity(self.all_people, tmstamp, self.db_conn)

    def __update_movement_time_series__(self, persons, date): 
        """
        Updates each person.today_schedule to a dictionary containing the timestamps of a given date and locations
        """
        time_in_sec = time.mktime(date)
        
        for person in persons:
            timestamp = time_in_sec
            newschedule = {}

            for j in range(24):
                try:
                    tp = person.timetable['monday'][0]
                    j1 = j
                except:
                    j1 = str(j)
                temp = timestamp + j*60*60
                if person.Status == 'Free' :
                    newschedule[time.localtime(temp)] = person.timetable[time.strftime("%A",time.localtime(temp)).casefold()][j1]
                elif person.Status == 'Quarentined' or person.Status == 'Isolation' :
                    newschedule[time.localtime(temp)] = person.residence_unit
                else :
                    building_id = person.Campus.sectors['Healthcare'].building_ids[0]
                    unit_id = random.choice(list(person.Campus.sectors['Healthcare'].Units_list[building_id].keys()))
                    newschedule[time.localtime(temp)] = person.Campus.sectors['Healthcare'].Units_list[building_id][unit_id]
            
            person.today_schedule = newschedule
