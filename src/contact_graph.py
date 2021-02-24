import os
import json
import datetime
import pandas as pd
import mysql.connector
from pyvis.network import Network

from .graph_utils import decayfunc, proximityfunc, CG_pm

# TODO: Cleanup, comments, functions

def getContacts(deviceid, time_ref):
	print("in getContacts")
	""" 
	Function print the nodes which came in contact with infected node in past few days. 
  
	Require two table named identity and activity to retrive the data and duration from parameters. 
  
	Parameters: 
	deviceid (string): Contains the device id
	time_ref (datetime): Reference time from which we want to check for the past duration days
  
	Returns: 
	None: Currently only prints, make changes in the last line to return value 
  
	"""

	# Establish connection to MySQL Server
	try:
		db_connection = CG_pm.database_conn
		'''
		db_connection = mysql.connector.connect(
			host      = CG_pm.hostname,
			user      = CG_pm.username,
			passwd    = CG_pm.password,
			database  = CG_pm.dbname
		)
		'''
		db_cursor = db_connection.cursor()

	except:
		print("Can't Connect to database, check credentials in parameters file")
	
	query = ("SELECT * FROM identity ")
	db_cursor.execute(query)
	df1=pd.DataFrame(db_cursor.fetchall())
	df1.columns= ['node','deviceid','student','rollno']
	dict_identity = dict(zip(df1.deviceid, df1.node))
	rev_dict_identity = dict(zip(df1.node, df1.deviceid ))
	#print(dict_identity)
	inf_node= dict_identity[deviceid]
	#print(inf_node)
	query = ("SELECT MIN(time) FROM activity")
	db_cursor.execute(query)
	row = db_cursor.fetchone()
	begin_time=row[0]
	query = ("SELECT * FROM activity WHERE time BETWEEN '{}' AND '{}'".format(max(begin_time,time_ref-datetime.timedelta(days=CG_pm.duration)),time_ref))  ## incomplete
	db_cursor.execute(query)
	df2=pd.DataFrame(db_cursor.fetchall())
	if df2.empty:
		print("Empty activity database, Try again with different date or deviceid")
		return
	df2.columns= ['slno','time','node','lat','long']
	#print(str(df2.iloc[0,1]))
	df_inf= df2[df2.node==inf_node]
	df2= df2[df2.node!=inf_node]
	score={}
	for i in range(len(df_inf)):
		time_inf= df_inf.iloc[i,1]
		score_tmp = decayfunc(time_inf,time_ref)
		df_tmp= df2[df2.time==time_inf]
		for j in range(len(df_tmp)):
			if proximityfunc(df_inf.iloc[i,3],df_inf.iloc[i,4],df_tmp.iloc[j,3],df_tmp.iloc[j,4]):
				try:
					score[df_tmp.iloc[j,2]]+= score_tmp
				except:
					score[df_tmp.iloc[j,2]]= score_tmp

	################## Bluetooth Contruction ##############
	#Bluetooth Connection and Score Generation
	try:
		with open(r'C:\Users\HP\Desktop\project\Contact_Graph\bluetooth.txt') as json_file:
			data1 = json.load(json_file)
			data1 = data1[deviceid]
			#print(data1)
			for time, arr in data1.items():
					time_obj = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
					if (time_ref-datetime.timedelta(days=CG_pm.duration)) > time_obj:
						continue
					df_time= df2[df2.time==time_obj]
					score_tmp= decayfunc(time_obj,time_ref)
					for dev_id in arr:
						if dev_id not in df_time.time:
							try:
								score[dict_identity[dev_id]]+= score_tmp
							except:
								score[dict_identity[dev_id]]= score_tmp
	except:
		print("File C:\Users\HP\Desktop\project\Contact_Graph\bluetooth.txt not found")

	#############################################imputed score addition ########
	"""query = ("SELECT * FROM imputed WHERE time BETWEEN '{}' AND '{}'".format(max(begin_time,time_ref-datetime.timedelta(days=CG_pm.duration)),time_ref))  ## incomplete
	db_cursor.execute(query)
	df_imp=pd.DataFrame(db_cursor.fetchall())
	if df_imp.empty:
		print("Empty imputed database")
	else:
		df_imp.columns= ['slno','time','node','lat','long']
		df_imp_inf= df_imp[df_imp.node==inf_node]
		df_imp= df_imp[df_imp.node!=inf_node]
		 ###### score when the missing data is of infected node #######
		for i in range(len(df_imp_inf)):
			time_inf= df_imp_inf.iloc[i,1]
			score_tmp = decayfuncimputed(time_inf,time_ref)
			df_tmp= df_imp[df_imp.time==time_inf]
			for j in range(len(df_tmp)):
				if proximityfuncimputed(df_imp_inf.iloc[i,3],df_imp_inf.iloc[i,4],df_tmp.iloc[j,3],df_tmp.iloc[j,4]):
					try:
						score[df_tmp.iloc[j,2]]+= score_tmp
					except:
						score[df_tmp.iloc[j,2]]= score_tmp
		"""
	#############################################

	node_list=[inf_node]
	label_list=[deviceid]
	color_list=["#C0392B"]
	value_list=[0]
	title_list=["Infected Node"]
	ans=sorted( ((v,k) for k,v in score.items()), reverse=True)
	edges_list=[]
	for (val,key) in ans:
		node_list.append(key)
		label_list.append(rev_dict_identity[key])
		color_list.append('#2E86C1')
		edges_list.append((int(inf_node),int(key),float(val)))
		value_list.append(val)
		title_list.append("Score: "+str(val))
		print("Name",df1[df1.node==key].iloc[0,2]," node no. => ",key," and score =>",val)
	#####Visualize###############
#	value_list[0]= max(value_list)*2
#	g= Network("500px", "500px",directed=False)
#	g.add_nodes(node_list,label=label_list,title=title_list,value=value_list,color=color_list)
#	g.add_edges(edges_list)
#	g.show("nx.html")
