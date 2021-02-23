import random
import numpy as np
import pandas as pd
import geopandas as GP
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point

def random_points_in_polygon(number, polygon):
    points = []
    min_x, min_y, max_x, max_y = polygon.bounds
    i = 0
    while i < number:
        point = Point(random.uniform(min_x, max_x), random.uniform(min_y, max_y))
        if polygon.contains(point):
            points.append(point)
            i += 1
    return points

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