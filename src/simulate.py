import random
import numpy as np

class Simulate():
    def __init__(self):
        self.SIMULATE   = True
        self.TODAY      = 1 

        super().__init__()

    def simulation(self):
        # Infect people intially

        # bookkeeping funks

        while (self.SIMULATE):
            self.__simulate_day__()

        
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

        # TODO (Varun)
        # for healthy persons normal schedule
        # for hosp/quar etc policy will be diff

        self.daily_transmissions()

        # TODO (Varun)
        # routine to spread virus using contact graph

        # save case stats after today's spreading

        self.TODAY += 1
        pass