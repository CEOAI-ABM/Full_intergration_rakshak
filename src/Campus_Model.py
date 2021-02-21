from .Non_Student import init_profs_from_schedule
from .person import person, professor, get_movement_time_series
from .utils import publish_loc, form_schedule, create_db_publish_locations

class Campus:
	def __init__(self):
		super(Campus, self).__init__()

		# Timetable Params
		self.Departments 				= self.pm.Departments
		self.Deptwise_Timetable 		= None # dept, year wise timetable

		# Building Params
        self.Number_Units               = self.pm.num_rooms
        self.Total_Num_Buildings        = len(self.Number_Units)
        self.Number_Workers             = self.pm.Number_Workers
        self.Height                     = self.pm.Height
        self.Location                   = [self.pm.xlist, self.pm.ylist]
        self.Daily_People_Expectation   = self.pm.Daily_People_Expectation
        self.RoomCodes                  = []
        self.Rooms                      = {}
        self.Index_Holder               = []
		self.Sectors 					= [] # list of objects
        self.Units_Placeholder          = {i:{} for i in range(self.Total_Num_Buildings)} # 
        self.People_In_Buildings        = [0]*(self.Total_Num_Buildings)

		# Campus Citizens 
		self.Students 					= None
		self.Profs						= None

	def initialize_campus(self):
		self.__initialize_sectors__()
        self.__initialize_units__()

		self.Deptwise_Timetable = form_schedule() 

		# Lists of students and profs
		self.__init_students__()
		self.__init_profs__(start_id=len(self.Students)+1)
		#NTS

		#print(students[0].get_timetable())
		#print(profs[1].daily_schedule_expected)

	def __initialize_sectors__(self):
		# TODO

    def __initialize_units__(self):
        k = 0
        for building in range(self.Total_Num_Buildings):
            self.Index_Holder.append(k)
            #self.Number_Workplaces[building] = np.round(np.random.normal(np.array(self.Daily_People_Expectation[building]),np.array(self.Daily_People_Expectation[building])/6)).astype(np.int)

            if(self.Number_Units[building]>0):
                temp_room_code = self.pm.df['Abbreviation'][building]
                if len(temp_room_code) != 0:
                    self.RoomCodes.append(temp_room_code.split(','))
                    #print(self.RoomCodes[-1])
                for j in range(len(self.Height[building])):
                    #print(len(self.Location[0][building]),j,self.Height[building])
                    self.Units_Placeholder[building][k] = Unit(j,building,self.Daily_People_Expectation[building][j],self.Number_Workers[building],self.Height[building][j],self.Location[0][building][j],self.Location[1][building][j],self)
                    if len(temp_room_code) != 0:
                        some_temp_no = int(j/(len(self.Height[building])//len(self.RoomCodes[-1])))
                        if some_temp_no >= len(self.RoomCodes[-1]): some_temp_no = len(self.RoomCodes[-1])-1
                        roomcode = self.RoomCodes[-1][some_temp_no]
                        self.Rooms[roomcode+str(j-((len(self.Height[building])//len(self.RoomCodes[-1])))*some_temp_no)]=self.Units_Placeholder[building][k]
                    k+=1

	def __init_students__(self):
		"""
		For initializing people & giving them their respective schedules
		Args:
			schedule(dict): containing year-wise classes+labs with slots & rooms
		"""
		residence_indices = [i for i in range(len(self.pm.description)) if self.pm.description[i]=='Residence']
		weights = [self.Number_Units[i] for i in residence_indices]

		# TODO: Remove all hard-coding
		ctr=1
		for dept in self.Departments:
			dept_schedule = self.Deptwise_Timetable[dept]
			for i in range(2, 5):
				for j in range(1,random.randrange(40, 60)):
					person_schedule = self.Deptwise_Timetable[dept][i]
					age = str(18 + (i-1) + random.choice([0,1]))
					
					hall = random.choices(residence_indices, weights)[0]
					room = random.randint(0,len(sectorptr.Height[hall])-1)
					junta = person(sectorptr=sectorptr, role="student", ID=ctr, age=age, year=j, schedule=person_schedule, dept=dept, residence=[hall, room])
					ctr += 1
					
					self.Students.append(junta)

	def __init_profs__(self, start_id):
		'''
		Takes the dict returned by form_schedule
		Assigns a prof to a course
		'''
		houseno = 0
		for i in schedule:
			dept_roomno = 0
			for j in schedule[i]:
				for k in schedule[i][j]:
					subj = {k: schedule[i][j][k]}
					dept = i
					lab = dept+str(dept_roomno)
					office_no = (len([d for d in self.Rooms if d[0:2]==dept])-dept_roomno-1)
					office=dept+str(office_no)
					someno = office_no
					while someno>0 and self.RoomNo_to_Unit(office).isclassroom == True:
						someno-=1
						office=dept+str(someno)
					else:
						if someno < 0:
							office = lab
					
					prof = professor(Campus=self, HouseNo=houseno, ID=start_id+houseno, dept=dept, schedule=subj, lab=lab, office=office)
					self.Profs.append(prof)
					
					houseno+=1
					dept_roomno+=1

	def RoomNo_to_Unit(self, room_name):
        if room_name[0] == 'V':
            code = room_name[0]
            number = room_name[1:]
        else:
            code = room_name[0:2]
            if code == 'NC':
                allrooms=['NC131', 'NC132', 'NC141', 'NC142', 'NC231', 'NC232', 'NC233', 'NC234', 'NC241', 'NC242', 'NC243', 'NC244', 'NC331', 'NC332', 'NC333', 'NC334', 'NC341', 'NC342', 'NC343', 'NC344', 'NC431', 'NC432', 'NC433', 'NC434', 'NC441', 'NC442', 'NC443', 'NC444']
                number = str(allrooms.index(room_name))
            elif code == 'NR':
                allrooms=['NR121', 'NR122', 'NR123', 'NR124', 'NR221', 'NR222', 'NR223', 'NR224', 'NR321', 'NR322', 'NR323', 'NR324', 'NR421', 'NR422', 'NR423', 'NR424']
                number = str(allrooms.index(room_name))
            elif code == 'S-':
                allrooms = ['S-123', 'S-125', 'S-126', 'S-127', 'S-136', 'S-216', 'S-122A', 'S-301', 'S-302']
                number = str(allrooms.index(room_name))
            elif len(room_name) == 5 and room_name[3]=='L':
                number = str(int(room_name[2]+room_name[4])-20)
            else:
                number = room_name[2:]
                #print(code+number)
        return self.Rooms[code+number]