import numpy as np
class Parameters:
    def __init__(self,classType):
        if classType=='Academic':
            self.Buildings = {0: 'MainBuilding',
                              1: 'Nalanda',
                              2: 'Aerospace Engineering',
                              3: 'Agricultural and Food Engineering',
                              4: 'Architecture and Regional Planning',
                              5: 'Biotechnology',
                              6: 'Chemical Engineering',
                              7: 'Civil Engineering',
                              8: 'Computer Science and Engineering',
                              9: 'Electronics and Electrical Communication Engg.',
                              10: 'Industrial and Systems Engineering',
                              11: 'Mechanical Engineering',
                              12: 'Metallurgical and Materials Engineering',
                              13: 'Mining Engineering',
                              14: 'Ocean Engg and Naval Architecture',
                              15: 'Advanced Technology Development Centre',
                              16: 'Center for Rural Development and Innovative Sustainable Technology',
                              17: 'Centre for Computational and Data Sciences',
                              18: 'Centre For Educational Technology',
                              19: 'Centre for Oceans, Rivers, Atmosphere and Land Sciences (CORAL)',
                              20: 'Centre For Theoretical Studies',
                              21: 'Centre of Excellence in Advanced Manufacturing Technology',
                              22: 'Centre of Excellence in Artificial Intelligence (AI)',
                              23: 'Centre of Excellence on Safety Engineering &amp; Analytics (COE-SEA)',
                              24: 'Cryogenic  Engineering',
                              25: 'Deysarkar Centre of Excellence in Petroleum Engineering',
                              26: 'Materials Science Centre',
                              27: 'P.K. Sinha Centre for Bioenergy and Renewables',
                              28: 'Rekhi Centre of Excellence for the Science of Happiness',
                              29: 'Rubber Technology',
                              30: 'Steel Technology Centre',
                              31: 'Bio Science',
                              32: 'Energy Science and Engineering',
                              33: 'Environmental Science and Engineering',
                              34: 'Nano Science and Technology',
                              35: 'Rajendra Mishra School of Engg Entrepreneurship',
                              36: 'Rajiv Gandhi School of Intellectual Property Law',
                              37: 'Ranbir and Chitra Gupta School of Infrastructure Design and Mngt.',
                              38: 'School of Water Resources',
                              39: 'Subir Chowdhury School of Quality and Reliability',
                              40: 'Vinod Gupta School of Management',
                              41: 'Takshashila',
                              42: 'Vikramshila',
                              43: 'Academy of Classical and Folk Arts',
                              44: 'Partha Ghosh Academy of Leadership',
                              45: 'Sir J C Bose Laboratory Complex'}
            self.Building_to_id = {}
            for k,v in self.Buildings.items():
                self.Building_to_id[v] = k

            self.pm = [[],[],[],[],[],[]] #(6 parameters to be returned to Academic())
            for i in range(len(self.Buildings)):
                rooms = np.random.randint(5,20)
                self.pm[0].append(rooms)
                self.pm[1].append(np.random.randint(5,50))
                self.pm[2].append(np.random.randint(0,5,rooms))
                self.pm[3].append(np.random.randint(-50,50,rooms))
                self.pm[4].append(np.random.randint(-50,50,rooms))
                self.pm[5].append(np.random.randint(0,50,rooms))

    def BuildingInfo(self,id=None,BuildingName=None):
        if BuildingName==None:
            self.Building_Name = self.Buildings[id]
            return self.Building_Name
        if id==None:
            self.id = self.Building_to_id[BuildingName]
            return {'id':self.id,'Num_Units': self.pm[0][self.id]}
    def returnParam(self):
        return self.pm


if __name__=='__main__':
    p = Parameters('Academic')
    print(p.returnParam()[2])
    print(p.BuildingInfo(BuildingName='MainBuilding'))
