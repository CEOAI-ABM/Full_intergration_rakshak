import os
import json
import datetime
import pandas as pd
import mysql.connector
from pyvis.network import Network

# from .graph_utils import decayfunc, proximityfunc, graphformation

def get_contacts_from_server(person, time, duration, db_conn):
	""" 
	Function print the nodes which came in contact with infected node in past few days. 
  
	Require two table named identity and activity to retrive the data and duration from parameters. 
  
	Parameters: 
	deviceid (string): Contains the device id
	time_ref (datetime): Reference time from which we want to check for the past duration days
  
	Returns: 
	None: List of nodes(contacts) and the correspondings edge weights
	"""

	# consider sending only cursor
	db_cursor = db_conn.cursor()
	 
	# TODO
	"""
	for day in range(duration):
		for hour in range(24):
			# get person's unit 
			db_cursor.execute("SELECT unit_id FROM activity WHERE node = %s WHERE time []") # temp
			unit = db_cursor.fetchone()[0]
			
			# get all people in that unit
			db_cursor.execute("SELECT node FROM activity WHERE unit_id = %s") # temp
			contacts += db_cursor.fetchall()
	"""

	# node list should be unique
	# edges = duration of contact 

	# close cursor?
	
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
