import json
import random
import numpy as np
import pandas as pd
import geopandas as GP
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

slots = json.load(open('data/Timetable/Schedule/slots.json'))

class Parameters:
    # make this code more systematic (only params to be declared in init, rest to be done in functions)
    def __init__(self, ShpFile, OtherFile):
        self.Departments                                = ['AE', 'AG', 'AR', 'BT', 'CE', 'CH',
                                                           'CS', 'CY', 'EC', 'EE', 'EX', 'GG',
                                                           'HS', 'IE', 'IM', 'MA', 'ME', 'MF',
                                                           'MI', 'MT', 'NA', 'PH', 'QE', 'QM']
        self.Number_Workers                             = []
        self.Floor                                      = []
        self.Daily_People_Expectation                   = []

        gdf                                             = GP.read_file(ShpFile)
        self.df                                         = pd.read_csv(OtherFile,na_filter=False)
        self.building_name                              = gdf['name']
        self.rooms_packing_fraction                     = [1 for i in range(len(self.building_name))]
        self.description                                = gdf['descriptio']
        self.coordinates, self.ref, self.polygons       = cal_coordinates(gdf)
        self.rooms                                      = []
        self.num_rooms_per_floor                        = list()
        self.heights                                    = list()
        self.xlist = []
        self.ylist = []

        self.__assign_num_rooms_heights__()

        self.__cal_rooms__(self.num_rooms_per_floor)

        self.__assign_coords__()

        self.__assign_remaining__()

        #self.pm = [self.num_rooms,[],[],self.xlist,self.ylist,[]] #(7 parameters to be returned to Sector())

    def __assign_remaining__(self):
        for i in range(len(self.building_name)):
            self.Number_Workers.append(np.random.randint(5,50))
            self.Floor.append([])
            
            for j in range(1, self.heights[i]+1):
                for k in range(self.num_rooms_per_floor[i]):
                    self.Floor[i].append(j)
                
            self.Daily_People_Expectation.append(np.random.randint(0, 50, self.num_rooms_per_floor[i]*self.heights[i]))


    def __assign_num_rooms_heights__(self):

        '''assigns number of rooms by taking reference of the lib and lbs if not known  through KGP Data - Sheet1.csv
        and randomly allocates no of floors if not known through KGP Data - Sheet1.csv
        '''

        lib_area                          = self.polygons[2].area #area of library
        lib_num_rooms_per_floor           = 20
        lbs_area                          = self.polygons[32].area #area of LBS Hall
        lbs_num_rooms_per_floor           = 130

        for i in range(len(self.building_name)):
            try:
                self.num_rooms_per_floor.append(int(self.df['number of rooms/floor'][i]))
                self.heights.append(int(self.df['height'][i]))
            except:
                if self.df['description'][i] == 'Academic':
                    mu = lib_num_rooms_per_floor*self.polygons[i].area/lib_area
                else:
                    mu = lbs_num_rooms_per_floor*self.polygons[i].area/lbs_area
                self.num_rooms_per_floor.append(int(abs(np.round(np.random.normal(mu,3,1)))))
                if self.num_rooms_per_floor[-1] == 0:
                    self.num_rooms_per_floor[-1] = 1
                self.heights.append(int(abs(np.round(np.random.normal(3,0.5,1)))))


    def __assign_coords__(self):
        j = 0
        for buil in self.rooms:
            self.xlist.append([i.x for i in buil]*self.heights[j])
            self.ylist.append([i.y for i in buil]*self.heights[j])
            j+=1


    def __cal_rooms__(self, no_rooms):
        for i in range(len(self.building_name)):
            points = random_points_in_polygon(no_rooms[i],self.polygons[i])
            self.rooms.append(points)
        return


def cal_coordinates(df):
    temp = []
    for i in range(len(df['geometry'])):
        temp.append(list(df['geometry'][i].exterior.coords))

    #print(temp[32])
    refx, refy = temp[32][0][1], temp[32][0][0]
    ref = [(refx * 100) % 100, (refy * 100) % 100]
    #print(ref)

    coordinates = []
    for i in range(len(temp)):
        build_cord = []
        for j in range(len(temp[i])):
            #x = (temp[i][j][0] * 100) % 100
            #y = (temp[i][j][1] * 100) % 100
            #xy = [round((x - ref[0]) * 100, 3), round((y - ref[1]) * 100, 3)]
            x = temp[i][j][0]
            y = temp[i][j][1]
            xy = [x,y]
            build_cord.append(xy)
        coordinates.append(build_cord)

    polygons = []
    for pointList in coordinates:
        poly = Polygon([(p[0], p[1]) for p in pointList])
        polygons.append(poly)

    return coordinates,ref,polygons


def random_points_in_polygon(number, polygon):
    from shapely.geometry import Point

    points = []
    min_x, min_y, max_x, max_y = polygon.bounds
    i = 0
    while i < number:
        point = Point(random.uniform(min_x, max_x), random.uniform(min_y, max_y))
        if polygon.contains(point):
            points.append(point)
            i += 1
    return points


if __name__=='__main__':
    ShpFilePath = "../data/shapes/kgpbuildings.shp"
    FilePath = "../data/Campus_data/KGP Data - Sheet1.csv"
    pm = Parameters(ShpFilePath,FilePath)
    k = 0
    while True:
        try:
            print(k,pm.building_name[k],"---- DESCRIPTION:",pm.description[k],"---- Number of Rooms per Floor:",pm.num_rooms_per_floor[k],"---- Heights of the building",pm.heights[k])
            k+=1
        except:
            break
