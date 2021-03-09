import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.legend import Legend
v = []
from day1viz import viz
v.append(viz)


def main():

    img = plt.imread("campus.png")
    cnt = 0
    for viz in v:
        x, y, h = [[], [], []]

        xarray = []
        yarray = []
        harray = []
        for k in range(24):
            try:
                x = [st[1] for st in viz[k]]
                y = [st[2] for st in viz[k]]
                h = []
                for st in viz[k]:
                    if st[3] == "Healthy":
                        if st[4] == 'student':
                            h.append('g^')
                        elif st[4] == 'faculty':
                            h.append('go')
                        else:
                            h.append('g+')
                    elif st[3] == 'Asymptomatic':
                        if st[4] == 'student':
                            h.append('r^')
                        elif st[4] == 'faculty':
                            h.append('r+')
                        else:
                            h.append('r,')
                    elif st[3] == 'Recovered':
                        if st[4] == 'student':
                            h.append('y^')
                        elif st[4] == 'faculty':
                            h.append('yo')
                        else:
                            h.append('y+')
                    elif st[3] == 'Died':
                        continue
                    else:
                        if st[4] == 'student':
                            h.append('b^')
                        elif st[4] == 'faculty':
                            h.append('bo')
                        else:
                            h.append('b+')
                xarray.append(x)
                yarray.append(y)
                harray.append(h)
            except:
                print("entered except")
                print(len(viz[12]))
        tm = 0
        finalpoints = []
        while tm < 24:
            newpoints = []
            j = 0
            while j<len(harray[tm]):
                newpoints.append(xarray[tm][j])
                newpoints.append(yarray[tm][j])
                newpoints.append(harray[tm][j])
                j+=1
            finalpoints.append(newpoints)
            tm+=1
        for k in [0,3,6,9,12,15,18,21]:
            fig, ax = plt.subplots(figsize=(19.20,10.80))

            ax = plt.axes(xlim=(87.293306,87.329261), ylim=(22.305830, 22.323165), aspect='equal')

            ax.imshow(img, extent=[87.293306,87.329261, 22.305830, 22.323165])
            Healthy = 0
            Asymptomatic = 0
            Symptomatic = 0
            Recovered = 0
            Died = 0

            for st in viz[k]:
                if st[3] =="Healthy":
                    Healthy+=1
                elif st[3] =="Asymptomatic":
                    Asymptomatic+=1
                elif st[3] == 'Recovered':
                    Recovered+=1
                elif st[3] == 'Died':
                    Died+=1
                else:
                    Symptomatic+=1
            lib = {0 : "Monday" ,1 : "Tuesday" ,2 : "Wednesday",3 : "Thursday",4 : "Friday" , 5 : "Saturday" , 6 : "Sunday"}
            ax.text(87.32, 22.322 ,'Number of Healthy people        : '+ str(Healthy))
            ax.text(87.32, 22.3215,'Number of Asymptomatic people : '+str(Asymptomatic))
            ax.text(87.32, 22.321 ,'Number of Symptomatic people  : '+str(Symptomatic))
            ax.text(87.32, 22.3205,'Number of Recovered people  : '+str(Recovered))
            ax.text(87.32, 22.32,'Number of Died people  : '+str(Died))
            print(str(k)+':00:00')
            ax.text(87.317, 22.307 ,'Day'+str(cnt+1) + '  ' +lib[cnt%7]+ '  '+str(k)+':00:00',fontsize=20,color='red')
            ax.plot(*(finalpoints[k]),markersize=3)
            h = plt.scatter(0, 0, marker='o', color='g')
            hh = plt.scatter(1, 0, marker='o', color='r')
            ho = plt.scatter(2, 0, marker='o', color='b')
            hl = plt.scatter(3, 0, marker='o', color='y')
            plt.legend((h, hh, ho,hl),('Healthy','Asymptomatic','Symptomatic','Recovered'),scatterpoints=1,loc='lower left',ncol=3,fontsize=8)
            ab = plt.scatter(1, 0, marker='^', color='g')
            ac = plt.scatter(2, 0, marker='o', color='g')
            ad = plt.scatter(3, 0, marker='+', color='g')
            leg = Legend( ax,[ab,ac,ad],['Student','Faculty','Staff'],scatterpoints=1,loc='lower right',ncol=3,fontsize=8)
            ax.add_artist(leg)
            #plt.show()
            #break
            plt.savefig(str(8*cnt+k//3)+'.png')

        cnt+=1




main()
