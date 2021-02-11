import os
import json
import random
import mysql.connector
import time

def total_students(course, grades, grades_18A, grades_18S, na_list):
    """Gives the count of total students present in the course 
        by adding all the grade allocations.
    
    Args:
        course (str): Course code
        grades,grades_18A,grades_18S (dict): Course Grade Report
        na_list (list): A list of the subjects with name (wherever possible)
                        whose strength couldn't be determined.
    
    Returns:
        strength (int): Strngth of the course.
    """
    strength = 0
    try:
        course_grades = grades[course]["grades"]

        print(course + " grades found")
        for grade in course_grades:
            print(course_grades[grade])
            strength = strength + course_grades[grade]

        return strength

    except KeyError:
        if course in grades_18A:
            course_grades = grades_18A[course]["grades"]

            print(course + " grades found")
            for grade in course_grades:
                print(course_grades[grade])
                strength = strength + course_grades[grade]

            return strength
        elif course in grades_18S:
            course_grades = grades_18S[course]["grades"]

            print(course + " grades found")
            for grade in course_grades:
                print(course_grades[grade])
                strength = strength + course_grades[grade]

            return strength
        else:
            try:
                txt = course + "- " + grades[course]["name"]
                if txt not in na_list:
                    na_list.append(txt)
            except KeyError:
                if course not in na_list:
                    na_list.append(course)

            print(course + " grades not found")
            return "NA"


def gen_timetable(file_path, schedule, grades, grades_18A, grades_18S):
    """Generates timetable through chill-zone + Kronos Json Files

    Args:
        file_path (str): path where the json are present.
        schedule (dict): Day-Wise course occupancy of the rooms
        grades,grades_18A,grades_18S (dict): Course Grade Report
    
    Returns:
        na_list (list): A list of the subjects with name (wherever possible)
                        whose strength couldn't be determined.

    Writes:
        occupancy.json: With strengths present in different rooms at
                        different times of the day.
    """
    na_list = []
    room_dict = {}
    for room in schedule:
        occupancy = schedule[room]
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        timmings = ['8-9','9-10','10-11','11-12','12-13','14-15','16,17','17-18']
        day_dict = {}
        for i in range(5):
            day = occupancy[i]
            stsrengths = {}
            for j in range(8):
                course  = day[j]
                if course != "":
                    print(course + " initiated")
                    strengths[timmings[j]] = (total_students(course, grades, grades_18A, grades_18S, na_list), course)
                else:
                    strengths[timmings[j]] = 0

            day_dict[days[i]] = strengths
        room_dict[room] = day_dict

    with open(file_path + "/occupancy_3.json", 'w') as fp:
        json.dump(room_dict, fp, sort_keys=True, indent=3)

    for entry in na_list:
        print(entry)

    return na_list

def form_subjects_real(file_path, subjects, grades, grades_18A, grades_18S):
    na_list = []
    final_subjects = {}

    for subject in subjects:
        temp = {}
        temp["strength"] = total_students(subject, grades, grades_18A, grades_18S, na_list)
        temp["slots"] = subjects[subject][0]
        temp['room'] = subjects[subject][1]
        final_subjects[subject] = temp
    
    with open(file_path + "/subjects.json",'w') as fp:
        json.dump(final_subjects, fp, sort_keys=True, indent=3)
    
    return na_list

def is_valid(subject):
    """ Checks whether the subject has sufficient information to be added to the 
    """
    if(subject["strength"]=="NA"):
        return False
    
    return True

def is_clash(slot,lab_slots):
    """ Checks for clash of slot with 
    """
    clash   = {'Q-Lab' : ['C3','B3','D3','D4'], "J-Lab" : ['H3','U3','U4'], "K-Lab" : ['D2','D3','D3','A3'], "L-Lab" : ['H2','H3','U3','U4'], "R-Lab" : ['F3','F4','G3','E3','E4'], "X-Lab" : ['X4'], "M-Lab" : ['C4','E3','E4','G3'], "N-Lab" : ['I2','V3','V3','V4'], "O-Lab" : ['E2','E4','F4','F3'], "P-Lab" : ['V4','V3','I2']}

    for entry in lab_slots:
        if(slot in clash[entry]):
            return True
    
    return False

def form_schedule(file_path=None,save=False):
    """ For generating shcedule for various departments

    Args:
        file_path(str): For storing the schedule.json
        save(bool): Whether to store the schedule  
    """

    depts   = ['AE', 'AG', 'AR', 'BT', 'CE', 'CH', 'CS', 'CY', 'EC', 'EE', 'EX', 'GG', 'HS', 'IE', 'IM', 'MA', 'ME', 'MF', 'MI', 'MT', 'NA', 'PH', 'QE', 'QM']
    rooms   = ['NC131', 'NC132', 'NC141', 'NC142', 'NC231', 'NC232', 'NC233', 'NC234', 'NC241', 'NC242', 'NC243', 'NC244', 'NC331', 'NC332', 'NC333', 'NC334', 'NC341', 'NC342', 'NC343', 'NC344', 'NC431', 'NC432', 'NC433', 'NC434', 'NC441', 'NC442', 'NC443', 'NC444', 'NR121', 'NR122', 'NR123', 'NR124', 'NR221', 'NR222', 'NR223', 'NR224', 'NR321', 'NR322', 'NR323', 'NR324', 'NR421', 'NR422', 'NR423', 'NR424', 'S-123', 'S-125', 'S-126', 'S-127', 'S-136', 'S-216', 'S-122A', 'S-301', 'S-302', 'V1', 'V2', 'V3', 'V4']
    slots_class   = ['A3', 'B3', 'C3', 'C4', 'D3', 'D4', 'E3', 'E4', 'F3', 'F4', 'G3', 'H3', 'S3', 'U3', 'U4', 'V3', 'V4', 'X4']
    slots_lab = ['J-Lab', 'K-Lab', 'L-Lab', 'M-Lab', 'N-Lab', 'O-Lab', 'P-Lab', 'Q-Lab', 'R-Lab', 'X-Lab']
    

    occupied = []
    schedule = {}

    for dept in depts:

        for i in range(2,5):
            temp_dict = {}
            year_schedule = {}
            lab_slot_taken = []
            occupied_slots = []

            # Allotting Lab Courses
            for j in range(1,random.randrange(4,6)):
                room    = dept + str(i) +  "L" + str(j)
                slot    = random.choice(slots_lab)

                while(slot in lab_slot_taken):
                    #room    = random.choice(rooms)
                    slot    = random.choice(slots_lab)
                else:
                    occupied_slots.append(slot)
                    lab_slot_taken.append(slot)
                    year_schedule[room] = {"slot" : slot, "room" : room}
            
            # Allotting Theory Courses
            for j in range(1,random.randrange(5,8)):
                room    = random.choice(rooms)
                slot    = random.choice(slots_class)

                ctr = 0
                while((slot in occupied_slots) and ((room + "_" + slot) in occupied) and is_clash(slot,lab_slot_taken) and ctr<50):
                    room    = random.choice(rooms)
                    slot    = random.choice(slots_class)
                    ctr = ctr+1
                else:
                    if(ctr>50):
                        while((slot in occupied_slots) or is_clash(slot,lab_slot_taken)):
                            slot = random.choice(slots_class)

                        else:
                            room = dept + "-room-" + str(j)
                            occupied.append(room + "_" + slot)
                            year_schedule[dept+ str(i) + "0" + str(j)] = {"slot" : slot, "room" : room}
                    else:
                        occupied.append(room + "_" + slot) 
                        occupied_slots.append(slot)
                        year_schedule[dept + str(i) + "0" + str(j)] = {"slot" : slot, "room" : room}
                        
                
            
            if(dept in schedule):
                schedule[dept].update({i:year_schedule})
            
            else:
                temp_dict[i] = year_schedule
                schedule[dept] = temp_dict
            
    return schedule

def create_db():
    pswd = input("Enter the password for your database server: ")
    mydb = mysql.connector.connect(host='localhost', user='root', passwd=pswd)
    stmt = 'CREATE DATABASE IF NOT EXISTS locations'
    mycursor = mydb.cursor()
    mycursor.execute(stmt)
    return 'locations', pswd


def create_db_publish_locations():
    pswd = input("Enter the password for your database server: ")
    mydb = mysql.connector.connect(host='localhost', user='root', passwd=pswd)
    mycursor = mydb.cursor()
    stmt = '''CREATE DATABASE IF NOT EXISTS current_locations'''
    mycursor.execute(stmt)
    stmt = '''USE current_locations'''
    mycursor.execute(stmt)
    stmt1 = '''DROP TABLE IF EXISTS people_locations'''
    mycursor.execute(stmt1)
    stmt2 = '''CREATE TABLE people_locations(
                        person_id INT,
                        timestamp VARCHAR(20),
                        person_role VARCHAR(10),
                        person_age INT,
                        person_status VARCHAR(20),
                        location_x DOUBLE,
                        location_y DOUBLE,
                        location_building_id INT,
                        location_unit_id INT,
                        PRIMARY KEY(person_id, timestamp)
                );
                '''
    mycursor.execute(stmt2)

    return 'current_locations', pswd

def publish_loc(persons, timestmp, dbname, pswd, insert=False):
    mydb = mysql.connector.connect(host='localhost', user='root', passwd=pswd, database=dbname)
    mycursor = mydb.cursor()
    if insert:
        stmt = '''INSERT INTO people_locations VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        data_ins = list()
        tmstmp = time.strftime("%Y-%m-%d %H:%M:%S",timestmp)
        for person in persons:
            unit  = person.schedule[timestmp]
            loc = unit.location
            x, y = loc.x, loc.y
            building_id = unit.Building
            unit_id = unit.Id + unit.Sector.Index_Holder[building_id]
            data_ins.append((person.ID, tmstmp, person.Role, person.Age, None, x, y, building_id, unit_id))
        mycursor.executemany(stmt, data_ins)
        mydb.commit()



def main():
    # Can be set to wherever the json files are present
    file_path = os.getcwd() + "/Timetable"

    with open(file_path + "/Schedule/schedule.json", 'r',encoding='utf8') as fp:
        schedule = json.load(fp)

    with open(file_path + "/Grades/courses.json", 'r',encoding='utf8') as fp:
        grades = json.load(fp)

    with open(file_path + "/Grades/2018Autumn.json", 'r',encoding='utf8') as fp:
        grades_18A = json.load(fp)

    with open(file_path + "/Grades/2018Spring.json", 'r',encoding='utf8') as fp:
        grades_18S = json.load(fp)

    with open(file_path + "/subjects.json",'r',encoding='utf8') as fp:
        subjects = json.load(fp)

    with open(file_path + "/Schedule/slots.json",'r',encoding='utf8') as fp:
        slots = json.load(fp)

    schedule = form_schedule(file_path)
    print(schedule)

    # na_list = form_subjects_real(file_path, subjects, grades, grades_18A, grades_18S)
    # na_list = gen_timetable(file_path, schedule, grades, grades_18A, grades_18S)
    
    # with open(file_path + "/na_subjects_list.txt",'w') as fp:
    #     for entry in na_list:
    #         fp.write(entry + "\n")


if __name__ == "__main__":
    main()
#    dbname, pwd = create_db_publish_locations()
#    print(dbname,pwd)
