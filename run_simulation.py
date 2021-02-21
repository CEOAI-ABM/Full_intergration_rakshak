import src 

if __name__ == '__main__':
    pm = src.Parameters(ShpFile='data/shapes/kgpbuildings.shp', OtherFile='data/Campus_data/KGP Data - Sheet1.csv') 
    src.StartSimulation(pm=pm)