import src
import sys
import json

if __name__ == '__main__':
    _, newid, data = sys.argv
    params = json.loads(data)
    pm = src.Parameters(ShpFile='data/shapes/kgpbuildings.shp', OtherFile='data/Campus_data/KGP Data - Sheet1.csv', **params)
    src.StartSimulation(pm=pm)
