import datetime
import mysql.connector

from .mysql_credentials import username, password

def create_db_publish_locations():
    mydb = mysql.connector.connect(host='localhost', user=username, passwd=password)
    mycursor = mydb.cursor()

    mycursor.execute("CREATE DATABASE IF NOT EXISTS Contact_Graph")
    mycursor.execute("USE Contact_Graph")
    mycursor.execute("DROP TABLE IF EXISTS `identity`")
    mycursor.execute("DROP TABLE IF EXISTS `activity`")

    '''
    stmt_i = """
    CREATE TABLE `identity` (
            `node` int NOT NULL AUTO_INCREMENT,
            `deviceid` varchar(45) NOT NULL,
            `student` varchar(45) DEFAULT NULL,
            `rollno` varchar(45) NOT NULL,
            PRIMARY KEY (`node`),
            UNIQUE KEY `deviceid_UNIQUE` (`deviceid`),
            UNIQUE KEY `Roll Number_UNIQUE` (`rollno`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
    """
    mycursor.execute(stmt_i)
    '''

    stmt_a = """
    CREATE TABLE `activity` (
        `slno` int NOT NULL AUTO_INCREMENT,
        `time` datetime NOT NULL,
        `node` int DEFAULT NULL,
        `latitude` decimal(8,6) NOT NULL,
        `longitude` decimal(9,6) NOT NULL,
        `unit_id` int 
        PRIMARY KEY (`slno`),
        UNIQUE KEY `slno_UNIQUE` (`slno`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
    """
    mycursor.execute(stmt_a)

    return mydb

def publish_identity(persons, mydb):
    mycursor = mydb.cursor()

    stmt = "INSERT INTO `identity` VALUES (%s, %s, %s, %s)"
    data_ins = list()
    
    for person in persons:
        data_ins.append((person.ID, str(person.ID), str(person.ID), str(person.ID)))
    
    mycursor.executemany(stmt, data_ins)
    mydb.commit()

def publish_activity(persons, timestmp, mydb):
    mycursor = mydb.cursor()
    stmt = "INSERT INTO `activity` (`time`, `node`, `latitude`, `longitude`, `unit_id`) VALUES (%s, %s, %s, %s, %s)"
    
    data_ins = []
    for person in persons:
        unit        = person.today_schedule[timestmp]
        unit_id     = unit.Id
        x, y        = unit.location.x, unit.location.y
        
        data_ins.append((datetime.datetime.fromtimestamp(time.mktime(timestmp)), person.ID, y, x, unit_id))

    mycursor.executemany(stmt, data_ins)
    mydb.commit()