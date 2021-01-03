import math
import numpy as np
from collections import Counter

class population_spread:
	"""A Class that stores the distribution grid and WiFi modems
		Takes 4 parameters:
		length of grid
		width of grid
		locations of the modems in the grid as a list of tupples: Ex [(1,2, (2, 3)]
		coverage of each modem as a list of numbers
	"""
	def __init__(self, pm):
		self.length=pm[0]
		self.width=pm[1]
		self.modem_locations=pm[2]
		self.modem_coverage=pm[3]
		self.distribution={}

	def dist_eval(self, num_people, num_to_distribute):
		"""We can define out distribution function w.r.t to the wifi_location point here
			I have used a uniform distribution in the wifirange.
		"""
		return (num_people+num_to_distribute-1)//num_to_distribute;


	def find_actual_distribution(self, wifi_data):
		"""Method that calculates the distribution given the wifi data
			wifi_data is a dictionary of thr form:
			{"Saturday":{"3:00-3:59": [2,3]}} the 2D list for each time stores the conunt of number of people connected to each modem
			the above implies => 2 people conneced to modem0 on saturday between 3 and 4 am;
					     3 people conneced to modem1 on saturday between 3 and 4 am;
		"""
		for day in wifi_data:
			self.distribution[day]={}
			for time, dist in wifi_data[day].items():
				self.distribution[day][time]=[[0 for i in range(self.width)] for j in range(self.length)]
				k=0
				for (x,y) in self.modem_locations:
					locations=[]
					for i in range (self.length):
						for j in range (self.width):
							if abs(x-i)+abs(y-j)<=self.modem_coverage[k]:
								locations.append((i,j))
					locations = sorted(locations, key=lambda temp: abs(x-temp[0])+abs(y-temp[1]), reverse=False)
					cnt=0; people=wifi_data[day][time][k]
					for (i,j) in locations:
						people_here=self.dist_eval(people,len(locations)-cnt)
						self.distribution[day][time][i][j]=self.distribution[day][time][i][j]+people_here
						people-=people_here
						cnt=cnt+1;
					k=k+1;
		return self.distribution;


if __name__=='__main__':
	WIFI={"Saturday":{}, "Sunday":{}, "Monday":{}, "Tuesday":{}, "Wednesday":{}, "Thursday":{}, "Friday":{}}

	for i in range(1):
		L=np.random.randint(5,10)
		W=np.random.randint(3,10)
		n=np.random.randint(1,8)
		locations=[]
		for j in range(n):
			locations.append((np.random.randint(0,L),np.random.randint(0,W)))
		locations=Counter(locations).keys()
		# print(locations)
		N=len(locations)
		coverage=[]
		for j in range(N):
			coverage.append(np.random.randint(1,L+W))
		# print(coverage)
		grid=population_spread([L,W,locations,coverage])
		data=WIFI.copy();
		for j in data:
			for k in range(24):
				data[j][str(k)+":00"+'-'+str(k)+":59"]=np.random.randint(1,100,N)
		grid.find_actual_distribution(data)
		print(grid.distribution)














