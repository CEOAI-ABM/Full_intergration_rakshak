import matplotlib.pyplot as plt
import matplotlib.animation as animation

from utils import form_schedule
from param_with_shp import Parameters
from sector import Sector
from person import __init_students__


def main():
    schedule = form_schedule()
    pm = Parameters('shapes/KgpBuildings.shp', 'Campus_data/KGP Data - Sheet1.csv')
    a = Sector(pm.returnParam())
    p = __init_students__(schedule, a)
    print(p[0].get_timetable())

    pa = []
    pb = []
#    print(p[0].get_timetable())
    for t in range(len(p)):
        pointa = []
        pointb = []
        for key, value in p[t].get_timetable().items():
            for aa, b in value.items():
                pointa.append(b.x)
                pointb.append(b.y)
        pa.append(pointa)
        pb.append(pointb)

    """pointa = []
    pointb = []
            #m = plt.scatter(b.x,b.y)
    for key,value in p[1].get_timetable().items():
        for aa,b in value.items():
            pointa.append(b.x)
            pointb.append(b.y)
    #plt.show()
    pa.append(pointa)
    pb.append(pointb)"""

#    print(pointa,pointb)
    fig = plt.figure()
    for i in a.ParamObj.polygons:
        plt.plot(*i.exterior.xy, lw=1)
    ax = plt.axes(xlim=(-300, 0), ylim=(0, 300), aspect='equal')
    x, y = [[], []]
    mat, = ax.plot(x, y, '.', markersize=1)

    def init():
        mat.set_data([], [])
        for i in a.ParamObj.polygons:
            ax.plot(*i.exterior.xy, lw=1)

    # animation function.  This is called sequentially
    def animate(i):
        x = [pa[k][i] for k in range(len(p))]
        y = [pb[k][i] for k in range(len(p))]
        mat.set_data(x, y)
        return mat,

    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=600)
    plt.show()


if __name__ == "__main__":
    main()
