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

