import math
import numpy as np
from collections import Counter
import time
from shapely.geometry import Point
import mysql.connector
import random

from param_with_shp import Parameters
from sector import Sector

class population_spread:
	"""A Class that stores the distribution dictionary and WiFi_data
		Input Type:
			Tupple
		Componente:
			pm[0]: wifi_data that has been extracted from the SQL table
			pm[1]: list of all the locations that the people of the campus can be at

	"""
	def __init__(self, pm, conn):

		self.data=pm[0];
		self.locations=pm[1];
		self.dist={};
		self.conn=conn;

		self.find_actual_distribution();

	def dist_eval(self, num_people, num_to_distribute):
		"""We can define out distribution function w.r.t to the wifi_location point here
			I have used a uniform distribution in the wifirange.
		"""
		return (num_people+num_to_distribute-1)//num_to_distribute;


	def find_actual_distribution(self):
		"""Method that calculates the distribution given the wifi data
			wifi_data is a dictionary of the form:
			{'struc_time_object':{(x,y): }} ->  This represents the number of people at location of
												(latitude, longitude) =(x,y) at the time represented by
												the time object;

		"""
		for record in self.data:
			self.locations = sorted(self.locations, key=lambda temp: abs(record[2]-temp[0].coords[0][0])+abs(record[3]-temp[0].coords[0][1]) + abs(temp[1]-record[6]), reverse=False);

			cnt=0;
			for location in self.locations:
				if abs(record[2]-location[0].coords[0][0])+abs(record[3]-location[0].coords[0][1]) + abs(location[1]-record[6])  <= record[4]:
					cnt=cnt+1;

			cnt=max(cnt,10);

			total=record[5];
			for i in range(cnt):

				people_here=self.dist_eval(total, cnt-i);
				total=total-people_here;

				if time.gmtime(record[0]*86400 + record[1]) not in self.dist.keys():
					self.dist[time.gmtime(record[0]*86400 + record[1])]={};

				if (self.locations[i][0].coords[0][0],self.locations[i][0].coords[0][1],self.locations[i][1]) not in self.dist[time.gmtime(record[0]*86400 + record[1])].keys():
					self.dist[time.gmtime(record[0]*86400 + record[1])][(self.locations[i][0].coords[0][0],self.locations[i][0].coords[0][1],self.locations[i][1])]=0;

				self.dist[time.gmtime(record[0]*86400 + record[1])][(self.locations[i][0].coords[0][0],self.locations[i][0].coords[0][1],self.locations[i][1])]+=people_here;

		cursor=self.conn.cursor();

		cursor.execute("DROP TABLE IF EXISTS distribution");
		self.conn.commit();

		cursor.execute("CREATE TABLE distribution (day INTEGER(200), seconds INTEGER(200), latitude FLOAT(200,30), longitude FLOAT(200,30), height INTEGER(200), people INTEGER(200))");		

		sqlform="INSERT INTO distribution (day, seconds, latitude, longitude, height, people) VALUES (%s, %s, %s, %s, %s, %s)"

		for TIME in self.dist:
			for location in self.locations:
				
				if (location[0].coords[0][0],location[0].coords[0][1], location[1]) not in self.dist[TIME].keys():
					self.dist[TIME][(location[0].coords[0][0],location[0].coords[0][1], location[1])]=0;


				cur_module=(((int)(time.mktime(TIME)))//86400, ((int)(time.mktime(TIME)))%86400, location[0].coords[0][0], location[0].coords[0][1], location[1], self.dist[TIME][(location[0].coords[0][0],location[0].coords[0][1], location[1])]);

				cursor.execute(sqlform, cur_module);		

		self.conn.commit();

def generate_random_location():
	"""Creates and assigns random coordinates to a Shapely Point
	Returns:
		Shapely Point : object
	"""
	latitude=random.uniform(-90,90);
	longitude=random.uniform(-180,180);

	temp=Point(latitude,longitude);

	return temp;

def Conn():
	"""Conn function to establish contact with MySQL server
	Returns:
		connection object: object contains mysql server information
	"""
	conn = mysql.connector.connect(user='root', password='welcome123', host='localhost', port=3306, auth_plugin='mysql_native_password', database='wifi');

	return conn;


if __name__=='__main__':

	conn=Conn();
	cursor=conn.cursor();
	cursor.execute("SELECT data.day, data.seconds, modules.latitude, modules.longitude, modules.coverage, data.people, modules.height FROM data LEFT JOIN modules ON data.name=modules.name");

	data=cursor.fetchall();

	pm = Parameters('shapes/kgpbuildings.shp','Campus_data/KGP Data - Sheet1.csv');
	a = Sector(pm.returnParam());

	locations = [];
	for building in a.Units_Placeholder:
	    for k in a.Units_Placeholder[building]:
	        locations.append((a.Units_Placeholder[building][k].location, a.Units_Placeholder[building][k].height));

	distribution=population_spread((data,locations),conn);

	# print(distribution.dist);

