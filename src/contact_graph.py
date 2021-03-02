import os
import json
import datetime
import time
import pandas as pd
import mysql.connector
from pyvis.network import Network

# from .graph_utils import decayfunc, proximityfunc, graphformation

def get_contacts_from_server(personid, time_datetime, db_conn, begin_time, duration=1):  # have to remove this hardcoding
	""" 
	Function print the nodes which came in contact with infected node in past few days. 
  
	Require two table named identity and activity to retrive the data and duration from parameters. 
  
	Parameters: 
	deviceid (string): Contains the device id
	time_ref (datetime): Reference time from which we want to check for the past duration days
  
	Returns: 
	None: List of nodes(contacts) and the correspondings edge weights
	"""


	db_cursor = db_conn.cursor()
	 
	# TODO
	'''
	start = time.time()
	query = ("SELECT MIN(time) FROM activity")
	db_cursor.execute(query)
	row = db_cursor.fetchone()
	begin_time=row[0]
	end = time.time()
	print ("Time elapsed to get min time:", end - start)
	'''
	#start = time.time()
	db_cursor.execute("SELECT unit_id,time FROM activity WHERE time BETWEEN '{}' AND '{}' AND node = {}".format(max(begin_time,time_datetime-datetime.timedelta(days=duration)),time_datetime, personid))
	units_times = db_cursor.fetchall()  #[(unit_id,time)]
	#end = time.time()
	#print ("Time elapsed to get inf_node's units:", end - start)


	#start = time.time()
	db_cursor.execute("SELECT node FROM activity WHERE node!={} AND (unit_id,time) IN (SELECT unit_id,time FROM activity WHERE time BETWEEN '{}' AND '{}' AND node = {})".format(personid,max(begin_time,time_datetime-datetime.timedelta(days=duration)),time_datetime,personid))
	temp_contacts = [i[0] for i in db_cursor.fetchall()]
	#end = time.time()
	#print("Time elapsed to get execute retriving inf_node's contacts for 24 timestamps at once:", end - start)
	contacts = dict()
	for i in temp_contacts:
		contacts[i] = contacts.get(i,0)+1
	node_list = list(contacts.keys())
	edges_list = []
	for i in node_list:
		edges_list.append(contacts[i])
	# node list should be unique
	# edges = duration of contact 


	#print("getting contacts done")



	db_cursor.close()
	return node_list, edges_list


def fullgraphplot(time_lower,time_upper):
	"""
    Function print the overall node graph within the selected time window. 
  
    Require two table named identity and activity to retrive the data. 
  
    Parameters: 
    time_lower (datetime): Lower time limit
    time_upper (datetime): Upper time limit
  
    Returns: 
    None: Currently only prints, make changes in the last line to return value 
  
    """

	edges_list,node_list,title_list = graphformation(time_lower,time_upper)
	node_size = []
	for i in range(len(node_list)):
		print("\nin fullgraphplot "+str(i)+"th element of node_list")
		node_size.append(5)
		g = Network(
            height="750px",
            width="100%",
            bgcolor="#222222",
            font_color="white")
	g.add_nodes(node_list,label=node_list,title=title_list, size= node_size)
	g.add_edges(edges_list)
	g.show("nx.html")
	return
