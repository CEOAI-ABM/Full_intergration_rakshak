import json
import os


class student:
    def __init__(self,yr,prog,dep): #still have to think about how to use prog
        self.year = yr
        self.program = prog
        self.dep = dep
    def default_timetable(self):
        pass

def recognize_year(s):
    return s[2]

class department:
    depth_courses = dict()
    def __init__(self,dep,subj):
        self.name = dep
        for sub in subj:
            yr = recognize_year(sub.code)
            if yr in self.depth_courses.keys():
                self.depth_courses[yr].append(sub)
            else:
                self.depth_courses[yr] = [sub]

class course:
    def __init__(self,course_num,slot,loc):
        self.code = course_num
        self.slot = slot
        self.class_location = loc

class Timetable:
    """Class for storing time table

    Args:
        occupancy (dict): Dictionary storing hourly strength 
                            present in classrooms across days
    """
    def __init__(self,file_name):

        with open(file_name,'r') as fp:
            self.occupancy = json.load(fp)

        print("Occupancy Dictionary loaded successfully")
    
    def get_strength(self,room,day,time):
        """Gets strength of students

        Args:
            room (str): Room No.
            day (str): Day of the Week
            time (str): Class timming in Railway format Eg. "1430"
        Returns:
            strength (int): No. students present at that time.
        """
        day = day.lower()
        room = room.upper()
        hour = time[0:2]
        # No classes on weekends & 1-2PM assumed
        if(day == 'saturday' or day == 'sunday' or hour == "13"):
            return 0

        # Getting the hour range
        timming = hour + "-" + str(int(hour)+1)

        try:
            return self.occupancy[room][day][timming]

        except KeyError:
            print("Room Data Unavailable")
        
        



if __name__ == "__main__":
    file_name = os.getcwd() + "/Timetable/occupancy_2.json"
    abc = Timetable(file_name)
    print(abc.get_strength("nc342","Thursday","1115"))
