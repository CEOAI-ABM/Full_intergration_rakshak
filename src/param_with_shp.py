import geopandas as GP
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import numpy as np
import pandas as pd
import random

class Parameters:
    def __init__(self, ShpFile, OtherFile):
        gdf = GP.read_file(ShpFile)
        self.df = pd.read_csv(OtherFile,na_filter=False)
        self.building_name = gdf['name']
        self.description = gdf['descriptio']
        self.coordinates, self.ref, self.polygons = cal_coordinates(gdf)
        self.rooms = []
        self.num_rooms = list()
        self.heights = list()
        lib_area = self.polygons[2].area #area of lib
        lbs_area = self.polygons[32].area #area of LBS
        for i in range(len(self.building_name)):
            try:
                self.num_rooms.append(int(self.df['number of rooms/floor'][i]))
                self.heights.append(int(self.df['height'][i]))
            except:
                if self.df['description'][i] == 'Academic':
                    mu = 20*self.polygons[i].area/lib_area
                else:
                    mu = 130*self.polygons[i].area/lbs_area
                self.num_rooms.append(int(abs(np.round(np.random.normal(mu,3,1)))))
                self.heights.append(int(abs(np.round(np.random.normal(3,0.5,1)))))
        self.cal_rooms(self.num_rooms)
        self.xlist = []
        self.ylist = []
        j = 0
        for buil in self.rooms:
            self.xlist.append([i.x for i in buil]*self.heights[j])
            self.ylist.append([i.y for i in buil]*self.heights[j])
            j+=1

        self.pm = [self.num_rooms,[],[],self.xlist,self.ylist,[],self] #(7 parameters to be returned to Sector())
        for i in range(len(self.building_name)):
                self.pm[1].append(np.random.randint(5,50))
                self.pm[2].append([])
                for j in range(1,self.heights[i]+1):
                    for k in range(self.num_rooms[i]):
                        self.pm[2][i].append(j)
                self.pm[5].append(np.random.randint(0,50,self.num_rooms[i]*self.heights[i]))


    def cal_rooms(self, no_rooms):
        for i in range(len(self.building_name)):
            points = random_points_in_polygon(no_rooms[i],self.polygons[i])
            self.rooms.append(points)
        return

    def returnParam(self):
        return self.pm


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
    ShpFilePath = "shapes/kgpbuildings.shp"
    FilePath = "Campus_data/KGP Data - Sheet1.csv"
    pm = Parameters(ShpFilePath,FilePath)
    k = 0
    while True:
        try:
            print(k,pm.building_name[k],"---- DESCRIPTION:",pm.description[k],"---- Number of Rooms:",pm.num_rooms[k],"---- Heights of the buildings",pm.heights[k])
            k+=1
        except:
            break
