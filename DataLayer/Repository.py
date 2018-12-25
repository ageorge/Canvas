from Model.User import User,UserRole
from Model.Course import Course,Assignment,Announcement,Grade,Files,StudentGrade
from DataLayer.DataAccess import DataAccess

class Repository:
    '''
    This class creates the query for all the functionality of the application and returns the required result
    '''
    def __init__(self):
        self.idac = DataAccess()

    '''
    Method to verify if the user is valid
    1. If yes, then the user object is returned
    2. If no, then None object is returned
    '''
    def verifyUser(self, username, password):
        if username != "":
            sql = "select u.username, u.name, u.password, r.rolename from User u inner join userroles ur on u.username = ur.username inner join roles r on r.roleid = ur.roleid where u.username = %s and u.password = %s"
            params = (username,password)
            result = self.idac.executeSelectStatement(sql,params)
            if result:
                return User(result[0])
            return None
        return False

    '''
    Method to get the user details
    '''
    def getUser(self, username):
        if username != "":
            sql = "select u.username, u.name, u.password, r.rolename from User u inner join userroles ur on u.username = ur.username inner join roles r on r.roleid = ur.roleid where u.username = %s"
            params = (username)
            result = self.idac.executeSelectStatement(sql,params)
            if result:
                return User(result[0])
            return None
        return False

    '''
    Method to retrieve all the courses of a particular student or admin 
    '''
    def getAllCoursesForStudent(self, user):
        if user.username != "":
            sql = "select uc.coursenum, c.coursename from usercourses uc inner join course c on c.coursenum = uc.coursenum where uc.username = %s and c.status='A'"
            params = (user.username)
            result = self.idac.executeSelectStatement(sql,params)
            if result:
                courses = []
                for course in result:
                    c = Course(course)
                    courses.append(c)
                return courses
            return None
        return False

    '''
    Method to retrieve all the courses of a particular student or admin 
    '''
    def getCourse(self, coursenum):
        if coursenum != 0:
            sql = "select uc.coursenum, c.coursename from usercourses uc inner join course c on c.coursenum = uc.coursenum where username = %s"
            params = (coursenum)
            result = self.idac.executeSelectStatement(sql,params)
            if result:
                courses = []
                for course in result:
                    c = Course(course)
                    courses.append(c)
                return courses
            return None
        return False

    '''
    Method to retrieve coursename for a coursenum
    '''
    def getCourseByCoursenum(self, coursenum):
        if coursenum != 0:
            sql = "select c.coursename from course c where c.coursenum = %s"
            params = (coursenum)
            result = self.idac.executeSelectStatement(sql,params)
            if result:
                return result[0][0]
            return None
        return False

    '''
    Method to retrieve all the announcements by coursenum
    '''
    def getAnnouncementsbyCourse(self, coursenum):
        if coursenum != 0:
            sql = "select * from announcement where coursenum = %s"
            params = (coursenum)
            result = self.idac.executeSelectStatement(sql,params)
            if result:
                announcements = []
                for announcement in result:
                    a = Announcement(announcement)
                    announcements.append(a)
                return announcements
            return None
        return False

    '''
    Method to retrieve all the assignments by coursenum
    '''
    def getAssignmentsbyCourse(self, coursenum):
        if coursenum != 0:
            sql = "select * from assignment where coursenum = %s"
            params = (coursenum)
            result = self.idac.executeSelectStatement(sql,params)
            if result:
                assignments = []
                for assignment in result:
                    a = Assignment(assignment)
                    assignments.append(a)
                return assignments
            return None
        return False

    '''
    Method to add a new announcement to the course
    '''
    def addAnnouncement(self, title, message, coursenum):
        sql = 'insert into announcement(announcementname, message, coursenum) values(%s,%s,%s)'
        params = (title, message, coursenum)
        result = self.idac.executeInsertUpdateDelete(sql,params)
        return result

    '''
    Method to add a new assignment to the course
    '''
    def addAssignment(self, new_assignment):
        sql = 'insert into assignment(assignmentname, assignmentdesc, assignmentdue, points, coursenum) values(%s,%s,%s,%s,%s)'
        params = (new_assignment.assignmentName, new_assignment.assignmentDesc, new_assignment.assignmentDue, new_assignment.assignmentPoints, new_assignment.assignmentCourse)
        result = self.idac.executeInsertUpdateDelete(sql,params)
        return result

    '''
    Method to add a new student to the course
    '''
    def addNewStudent(self, user,roleid ,coursenum):
        sql = 'insert into user(username, name, password) values(%s,%s,%s)'
        params = (user.username, user.name, user.password)
        result = self.idac.executeInsertUpdateDelete(sql,params)
        if result > 0:
            sql = 'insert into userroles(username, roleid) values(%s,%s)'
            params = (user.username, roleid)
            result = self.idac.executeInsertUpdateDelete(sql,params)
            if result > 0:
                sql = 'insert into usercourses(username, coursenum) values(%s,%s)'
                params = (user.username, coursenum)
                result = self.idac.executeInsertUpdateDelete(sql,params)
        return result

    '''
    Method to add an existing student to the course
    '''
    def addExistingStudent(self, user,coursenum):
        sql = 'insert into usercourses(username, coursenum) values(%s,%s)'
        params = (user.username, coursenum)
        result = self.idac.executeInsertUpdateDelete(sql,params)
        return result

    '''
    Method to get all the students in a course
    '''
    def getAllStudentsinaCourse(self, coursenum):
        if coursenum != 0:
            sql = "select u.username, u.name, u.password, r.rolename from usercourses uc inner join user u on u.username = uc.username inner join userroles ur on ur.username = u.username inner join roles r on r.roleid = ur.roleid where coursenum = %s"
            params = (coursenum)
            result = self.idac.executeSelectStatement(sql,params)
            if result:
                students = []
                for stu in result:
                    a = User(stu)
                    students.append(a)
                return students
            return None
        return False

    '''
    Method to get all the files for a course
    '''
    def getAllFilesForCourse(self,coursenum):
        if coursenum != 0:
            sql = "select f.fileid, f.filename, f.filepath from files f where coursenum = %s"
            params = (coursenum)
            result = self.idac.executeSelectStatement(sql,params)
            if result:
                files = []
                for f in result:
                    fi = Files(f)
                    files.append(fi)
                return files
            return None
        return False

    '''
    Method to return a file by fileID
    '''
    def getFilebyId(self,fileid):
        if fileid != 0:
            sql = "select filename, filepath from files where fileid = %s"
            params = (fileid)
            result = self.idac.executeSelectStatement(sql,params)
            if result:
                file = Files()
                file.fileId = fileid
                file.fileName = result[0][0]
                file.filePath = result[0][1]
                return file
            return None
        return False

    '''
    Method to add a new file to the course
    '''
    def addFile(self, new_file, coursenum):
        sql = 'insert into files(filename, filepath, coursenum) values(%s,%s,%s)'
        params = (new_file.fileName, new_file.filePath, coursenum)
        result = self.idac.executeInsertUpdateDelete(sql,params)
        return result

    '''
    Method to get all the grades for a student by course
    '''
    def getAllGradesForStudent(self,user,coursenum):
        if user and coursenum != 0:
            sql = "select a.assignmentname, g.gradepoint from studentgrades g inner join assignment a on a.assignmentid = g.assignmentid where g.username = %s and g.coursenum = %s"
            params = (user.username, coursenum)
            result = self.idac.executeSelectStatement(sql,params)
            if result:
                grades = []
                for g in result:
                    gr = Grade(g)
                    grades.append(gr)
                return grades
            return None
        return False

    '''
    Method to get all grades for an assignment for all students
    '''
    def getGradesForAssignment(self,coursenum,assignmentID):
        if coursenum != 0 and assignmentID != 0:
            sql = 'select uc.username, g.gradepoint, g.assignmentid from usercourses uc join userroles r on uc.username = r.username left join studentgrades g on uc.username = g.username where uc.coursenum = %s and r.roleid = 200'
            params = (coursenum)
            result = self.idac.executeSelectStatement(sql,params)
            people = self.getAllStudentsinaCourse(coursenum)
            if result:
                grades = []
                for g in result:
                    if g[2] == assignmentID:
                        gr = StudentGrade(g)
                        grades.append(gr)
                # include students who have yet to receive a grade
                for p in people:
                    flag = False
                    for g in grades:
                        if p.username == g.username:
                            flag = True
                            break
                    if flag == False and p.rolename != 'admin':
                        em = StudentGrade([p.username,None])
                        grades.append(em)
                return grades
            return None
        return False

    '''
    Method to find the grade of a student by assignmentid
    '''
    def findGrade(self,username,coursenum,assignmentid):
        sql = 'select gradepoint from studentgrades where username=%s and coursenum=%s and assignmentid=%s'
        params = (username,coursenum,assignmentid)
        res = self.idac.executeSelectStatement(sql,params)
        if res:
            return float(res[0][0])
        else:
            return None

    '''
    Method to add a new grade to a student for an assignment
    '''
    def addStudentGrade(self, username, coursenum, assignmentid, points):
        grade = self.findGrade(username,coursenum,assignmentid)
        result = None
        if grade:
            sql = 'update studentgrades set gradepoint = %s where username = %s and coursenum = %s and assignmentid = %s'
            params = (points,username,coursenum,assignmentid)
            result = self.idac.executeInsertUpdateDelete(sql,params)
        else:
            sql = 'insert into studentgrades values(%s,%s,%s,%s)'
            params = (username,coursenum,assignmentid,points)
            result = self.idac.executeInsertUpdateDelete(sql,params)
        return result

    '''
    Method to update password for a user
    '''
    def changePassword(self,username, newpass):
        sql = 'update user set password = %s where username = %s'
        params = (newpass,username)
        result = self.idac.executeInsertUpdateDelete(sql,params)
        return result


r = Repository()
res = r.findGrade('ageorge',1002,2003)
print(res)
