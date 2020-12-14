class student:
    def __init__(self,yr,prog,dep): #still have to think about how to use prog
        self.year = yr
        self.program = prog
        self.dep = dep
    def default_timetable(self):
        return self.dep.depth_courses[str(self.year)]

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


#adding a comment here