from . import spatial
from . import parameter as param

def Run():
    prm = param.Param()
    spt  = spatial.Spatial(pm=prm)
