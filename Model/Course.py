'''
This file contains model classes related to a course as per database or screen design
1. course
2. Assignment
3. Grade
4. Announcements
5. Files
6. StudentGrade
'''

from datetime import datetime

class Course:
    def __init__(self, course):
        self.coursenum = int(course[0])
        self.coursename = str(course[1])

    def __str__(self):
        s = str(self.coursenum) + " | " + self.coursename;
        return s


class Assignment:
    def __init__(self, assignment = None):
        if assignment:
            self.assignmentID = int(assignment[0])
            self.assignmentName = assignment[1]
            self.assignmentDesc = assignment[2]
            self.assignmentDue = assignment[3]
            self.assignmentPoints = int(assignment[4])
            self.assignmentCourse = int(assignment[5])
        else:
            self.assignmentID = 0
            self.assignmentName = ''
            self.assignmentDesc = ''
            self.assignmentDue = ''
            self.assignmentPoints = 0
            self.assignmentCourse = 0

    def __str__(self):
        s = str(self.assignmentID) + "|" + self.assignmentName + "|" + self.assignmentDesc + "|" + str(self.assignmentDue) + "|" + str(self.assignmentPoints) + "|" + str(self.assignmentCourse)
        return s

class Grade:
    def __init__(self, grade = None):
        if grade:
            self.assignment = grade[0]
            self.points = float(grade[1])
        else:
            self.assignment = ''
            self.points = '-'

    def __str__(self):
        s = str(self.assignment) + '|' + str(self.points)
        return s

class Announcement:
    def __init__(self, announcement = None):
        if announcement:
            self.announcementID = int(announcement[0])
            self.announcementName = announcement[1]
            self.announcementDate = announcement[2]  # The object from the database is received as DateTime object
            self.message = announcement[3]
            self.courseNum = int(announcement[4])
        else:
            self.announcementID = 0
            self.announcementName = ''
            self.announcementDate = datetime.now()
            self.message = ''
            self.courseNum = 0

    def __str__(self):
        s = str(self.announcementID) + "|" + self.announcementName + "|" + str(self.announcementDate) + "|" + self.message + "|" + str(self.courseNum)
        return s


class Files:
    def __init__(self, file = None):
        if file:
            self.fileId = int(file[0])
            self.fileName = file[1]
            self.filePath = file[2]
        else:
            self.fileId = 0
            self.fileName = ''
            self.filePath = ''

class StudentGrade:
    def __init__(self,grade = None):
        if grade:
            self.username = grade[0]
            if grade[1]:
                self.point = float(grade[1])
            else:
                self.point = '-'
        else:
            self.username = ''
            self.point = '-'

    def __contains__(self, item):
        if item == self.username:
            return True
        else:
            return False

    def __str__(self):
        s = str(self.username) + '|' + str(self.point)
        return s
