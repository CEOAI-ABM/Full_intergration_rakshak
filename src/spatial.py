import numpy as np

class Spatial(object):
    def __init__(self,pm):
        """Initialization of Spatial Class

        Args:
            pm ([type]): [description]
        """
        self.length     = pm.n
        self.width      = pm.m
        self.max_height = pm.h

        self.prob_dist  = np.ones((self.length,self.width,self.max_height))*(1/(self.length*self.width*self.max_height))
        self.heights    = pm.heights

        self.density    = np.ones((self.length,self.width,self.max_height))

    def compute_prob_dist(self,density=None):
        """[summary]

        Args:
            density ([type], optional): [description]. Defaults to None.
        """
        if density is None:
            self.prob_dist = self.density/(np.sum(self.density))
        else:
            self.density = density
            self.prob_dist = self.density/(np.sum(self.density))


class Grid():
    def __init__(self, pm):
        """ Initialization of grid class 

            Args :
            pm[0] is length of the building
            pm[1] is width of the building
            pm[2] is heights of building which is a 2d array representing maximum height attained by building at each place

        """
        self.length = pm[0]
        self.width = pm[1]
        self.heights = pm[2]

class SubGrid():
    def __init__(self ,pm):
        """ Initialization of grid class with subsquares 

            Args :
            pm[0] is length of the building
            pm[1] is width of the building
            pm[2] , pm[3] are used for knowing how the grid is divided into subsquares i.e., how much it is zoomed 
            pm[4] is heights of building which is a 4d array representing maximum height attained by building at each place
            
        """
        self.length = pm[0]
        self.width = pm[1]
        self.length1=pm[2]
        self.width1 = pm[3]
        self.heights = pm[4]

class SubSubGrid():
    def __init__(self ,pm):
        """ Initialization of grid class with subsquares divided into subsquares

            Args :
            pm[0] is length of the building
            pm[1] is width of the building
            pm[2] , pm[3] are used for knowing how the grid is divided into subsquares i.e., how much it is zoomed 
            pm[4] , pm[5] are used for knowing how the subsquares are further divided into subsquares 
            pm[6] is heights of building which is a 6d array representing height at each place
            
        """
        self.length = pm[0]
        self.width = pm[1]
        self.length1=pm[2]
        self.width1 = pm[3]
        self.length2 = pm[4]
        self.width2 = pm[5]
        self.heights = pm[6]
