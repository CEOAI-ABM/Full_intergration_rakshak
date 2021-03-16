import src 
import json
from simulator import master, parameters_shape
import sys
from multiprocessing import Value

if __name__ == '__main__':
    _, saveid, data = sys.argv
    params = json.loads(data)
    filepath = params.get("filepath", None)
    if "SIMULATION_DAYS" in params:
        params["SIMULATION_DAYS"] = Value('i', int(params["SIMULATION_DAYS"]))
   
    

    params["INPUT_SHAPEFILE"] = False
    params["SHOW_MAP"] = False
    
        

    pm = src.Parameters(ShpFile='data/shapes/kgpbuildings.shp', OtherFile='data/Campus_data/KGP Data - Sheet1.csv',**params) 
    src.StartSimulation(pm=pm)