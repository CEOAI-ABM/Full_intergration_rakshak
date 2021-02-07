import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

from utils import form_schedule
from param_with_shp import Parameters
from sector import Sector
from person import __init_students__
from Non_Student import init_profs_from_schedule


def main():
    schedule = form_schedule()
    pm = Parameters('shapes/kgpbuildings.shp', 'Campus_data/KGP Data - Sheet1.csv')
    a = Sector(pm.returnParam())
    p = __init_students__(schedule, a)
    profs = init_profs_from_schedule(schedule,a)
    print(p[0].get_timetable())
    print(profs[1].daily_schedule_expected)

    pa = []
    pb = []
#    print(p[0].get_timetable())
    for t in range(len(p)):
        pointa = []
        pointb = []
        for key, value in p[t].get_timetable().items():
            if key not in ['monday'] :
                continue
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

    for t in range(len(profs)):
        pointa = []
        pointb = []
        for key, value in profs[t].daily_schedule_expected.items():
            if key not in ['monday'] :
                continue
            for aa, b in value.items():
                pointa.append(b.x)
                pointb.append(b.y)
        pa.append(pointa)
        pb.append(pointb)

#    print(pointa,pointb)
    fig = plt.figure()
    for i in a.ParamObj.polygons:
        plt.plot(*i.exterior.xy, lw=1)
    ax = plt.axes(xlim=(-300, 0), ylim=(0, 300), aspect='equal')
    x, y = [[], []]
    mat, = ax.plot(x, y, '.', markersize=1)

    def init():
        mat.set_data([pa[k][0] for k in range(len(p)+len(profs))], [pb[k][0] for k in range(len(p)+len(profs))])
        for i in a.ParamObj.polygons:
            ax.plot(*i.exterior.xy, lw=1)
        return mat,

    xarray = []
    yarray = []
    numframe = 20
    totframes = 0
    for i in range(numframe*25):
        try:
            if i % numframe == 0:
                j = i//numframe
                x = [pa[k][j] for k in range(len(p)+len(profs))]
                y = [pb[k][j] for k in range(len(p)+len(profs))]
            else:
                m = i%numframe
                n = numframe-m
                x = [(n*pa[k][i//numframe]+m*pa[k][(i//numframe)+1])/numframe+np.random.normal(0,0.2,1) for k in range(len(p)+len(profs))]
                y = [(n*pb[k][i//numframe]+m*pb[k][(i//numframe)+1])/numframe+np.random.normal(0,0.2,1) for k in range(len(p)+len(profs))]
            xarray.append(x)
            yarray.append(y)
            totframes+=1
        except:
            break

    # animation function.  This is called sequentially
    def animate(i):
        x = xarray[i]
        y = yarray[i]
        mat.set_data(x, y)
        return mat,

    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=20, blit=True, repeat=False, save_count=totframes)
#    writergif = animation.PillowWriter(fps=40)
#    anim.save('student_and_prof.gif',writer=writergif)
    plt.show()


if __name__ == "__main__":
    main()
