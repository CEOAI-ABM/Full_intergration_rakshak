import os
import json

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
            return ("NA: " + course)


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
            strengths = {}
            for j in range(8):
                course  = day[j]
                if course != "":
                    print(course + " initiated")
                    strengths[timmings[j]] = total_students(course, grades, grades_18A, grades_18S, na_list)
                else:
                    strengths[timmings[j]] = 0

            day_dict[days[i]] = strengths
        room_dict[room] = day_dict

    with open(file_path + "/occupancy_2.json", 'w') as fp:
        json.dump(room_dict, fp, sort_keys=True, indent=3)

    for entry in na_list:
        print(entry)

    return na_list

def main():
    # Can be set to wherever the json files are present
    file_path = os.getcwd() + "/Timetable"

    with open(file_path + "/Schedule/schedule.json", 'r') as fp:
        schedule = json.load(fp)

    with open(file_path + "/Grades/courses.json", 'r') as fp:
        grades = json.load(fp)

    with open(file_path + "/Grades/2018Autumn.json", 'r') as fp:
        grades_18A = json.load(fp)

    with open(file_path + "/Grades/2018Spring.json", 'r') as fp:
        grades_18S = json.load(fp)

    na_list = gen_timetable(file_path, schedule, grades, grades_18A, grades_18S)

    with open(file_path + "/na_subjects_list.txt",'w') as fp:
        for entry in na_list:
            fp.write(entry + "\n")


if __name__ == "__main__":
    main()
