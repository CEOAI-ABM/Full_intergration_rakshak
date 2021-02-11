from random import Random
import random
from shapely.geometry import Point
import mysql.connector
import hashlib
import time
import numpy as np

class wifimodule(Random):
	"""Stores info about a specific wifi module(router):
	"""	
	def __init__(self,module_name,seed=None):
		"""3 Parameters	
			module_name is the ID of the router
			Seed help generate the value of number of people connected to this router, the coverage and height.
			location is the location of the router (it is a shapely point object);
		"""
		super().__init__();

		self.module_name=module_name;
		self.seed=seed if seed!=None else self.generate_seed();
		self.location=Point(0,0);
		self.coverage=abs(self.gauss(0.0005,0.0002));
		self.height=self.randint(1,5);

		super().seed(seed);

	def generate_seed(self):
		"""Generates a random seed based on the module name
		Returns:
			int:a seed for the random module
		""" 
		seed=int(hashlib.sha256(str(self.module_name).encode('utf-8')).hexdigest(), 16) % 10**6;

		return seed;

	def get_value(self):
		"""
		returns some random int value based on the seed
		Returns:
			int: value
		"""
		value=super().randint(10,100);

		return value;

def Conn():
	"""Conn function to establish contact with MySQL server
	Returns:
		connection object: object contains mysql server information
	"""
	conn = mysql.connector.connect(user='root', password='welcome123', host='localhost', port=3306, auth_plugin='mysql_native_password');

	cursor=conn.cursor();

	cursor.execute("DROP DATABASE IF EXISTS wifi");

	conn.commit();

	cursor.execute("CREATE DATABASE wifi");

	conn.commit();

	conn = mysql.connector.connect(user='root', password='welcome123', host='localhost', port=3306, auth_plugin='mysql_native_password', database='wifi');

	return conn;

def generate_random_location():
	"""Creates and assigns random coordinates to a Shapely Point
	Returns:
		Shapely Point : object 
	"""
	latitude=random.uniform(87.29398,87.3233);
	longitude=random.uniform(22.30806,22.32312);

	temp=Point(latitude,longitude);

	return temp;

def generate_modules(parameters,conn):
	"""Based on parameters generate a set of wifi modules
	Args:
		parameters(object): Should contain the information regarding the wifi modules
		Conn(object): object contains mysql server information
	Returns:
		list: list of wifimodule objects
	"""
	cursor=conn.cursor();

	cursor.execute("DROP TABLE IF EXISTS modules");
	cursor.execute("DROP TABLE IF EXISTS data");

	conn.commit();

	cursor.execute("CREATE TABLE modules (name INTEGER(200), latitude FLOAT(200,30), longitude FLOAT(200,30), height INTEGER(200), coverage FLOAT(200,30))");
	cursor.execute("CREATE TABLE data (name INTEGER(100), day INTEGER(100), seconds INTEGER(100), people INTEGER(100))");

	wifi_list=[];

	sqlform="INSERT INTO modules (name, latitude, longitude, height, coverage) VALUES (%s, %s, %s, %s, %s)"

	for each_module in parameters:

		# print(loc);
		loc=generate_random_location()
		temp=wifimodule(each_module.name);
		temp.location=loc;
		wifi_list.append(temp);
		cur_module=(temp.module_name, temp.location.coords[0][0], temp.location.coords[0][1], temp.height, temp.coverage);
		cursor.execute(sqlform, cur_module);

	conn.commit();

	return wifi_list;

def get_from_my_sql_table(conn):
	"""returns the wifi_list that was stored in the modules SQL Table
	Args:
		Conn(object): object contains mysql server information
	Returns:
		list: list of wifimodule objects
	"""
	cursor=conn.cursor();

	wifi_list=[];

	cursor.execute("SELECT * FROM modules");
	modules=cursor.fetchall();

	for each_module in modules:

		loc=Point(each_module[1],each_module[2]);
		temp=wifimodule(each_module[0]);
		temp.coverage=each_module[3];
		temp.location=loc;
		wifi_list.append(temp);

	return wifi_list;

def populate(parameters,wifi_list,conn):
	"""Populates a mysql data table
	Args:
		parameters(list): list of several struct_time objects
		wifi_list(list): List of wifimodules from generate_modules
		conn(object): connection object contains mysql server information
	"""
	cursor=conn.cursor();

	sqlform="INSERT INTO data (name, day, seconds, people) VALUES (%s, %s, %s, %s)"

	for each_time in parameters:

		for each_module in wifi_list:

			day=((int)(time.mktime(each_time)))//86400;
			seconds=((int)(time.mktime(each_time)))%86400;

			cur_stamp=(each_module.module_name, day, seconds, each_module.get_value());

			# print(cur_stamp);

			cursor.execute(sqlform,cur_stamp);

	conn.commit();
	
def repopulate(parameters,conn):
	"""RePopulates a mysql data table
	Args:
		parameters(object): Parameters
		conn(object): connection object contains mysql server information
	"""
	wifi_list=get_from_my_sql_table(conn);

	cursor=conn.cursor();
	cursor.execute("DELETE FROM data");
	conn.commit();

	populate(parameters,wifi_list,conn);

if __name__=='__main__':


	class online_module(object):
		def __init__(self,name):
			self.name=name;

	conn=Conn();

	N=random.randint(3000,3500);
	
	pms=[];
	for i in range(1,N):
		pms.append(online_module(i));
	wifi_list=generate_modules(pms,conn);

	start_time=time.strptime("01 Jan 2021", "%d %b %Y");
	stop_time=time.strptime("31 Mar 2021", "%d %b %Y");
	
	parameters=[];

	for i in range(int(time.mktime(start_time)),int(time.mktime(stop_time)),1800):
		parameters.append(time.gmtime(i));

	populate(parameters,wifi_list,conn);













