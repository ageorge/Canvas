from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from DataLayer.Repository import Repository
from Model.Course import Assignment,Files
from Model.User import User
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

# Below are the global variables to be used among the different screens
repo = Repository()
user = None
courses = None
coursenum = 0
sm = None
path = '/Users/anitageorge/Desktop/canvas'

class HomeScreen(Screen):
    '''
    This is the initial home screen of the canvas application
    '''
    pass


class CourseScreenStudent(Screen):
    '''
    This is the screen to display various options for each course for a STUDENT
    '''
    # This method clears the previous messages from the screen
    def clear(self):
        self.ids['msg'].text = ''

    # This method sets up the screen with initial data
    def initial(self):
        global user, coursenum
        coursename = repo.getCourseByCoursenum(coursenum)
        self.ids['info'].text = 'Welcome ' + user.username + " to " + coursename

    # This method creates a popup with the list of announcements
    def displayAnnouncements(self):
        global coursenum
        global user
        if coursenum != 0:
            announcements = repo.getAnnouncementsbyCourse(coursenum)
            mylayout = GridLayout(cols = 2)
            msg = Popup(title='Announcements',content=mylayout)
            msg.open()
            if announcements:
                for ann in announcements:
                    label = Label(text=str(ann.announcementName + "\n" + str(ann.announcementDate)))
                    label.size_hint_y = None
                    mylayout.add_widget(label)
                    label = Label(text=str(ann.message))
                    label.size_hint_y = None
                    mylayout.add_widget(label)
            else:
                label = Label(text='There are no announcements')
                label.size_hint_y = None
                mylayout.add_widget(label)
            close = Button(text='OK')
            close.size_hint_y = None
            close.bind(on_press=msg.dismiss)
            mylayout.add_widget(close)
        else:
            self.manager.current = 'DB'

    # This method creates a popup with the list of assignments
    def displayAssignments(self):
        global coursenum, user
        if coursenum != 0:
            assignments = repo.getAssignmentsbyCourse(coursenum)
            mylayout = GridLayout(cols = 3)
            msg = Popup(title='Assignments',content=mylayout)
            msg.open()
            label = Label(text="Assignment")
            label.size_hint_y = None
            mylayout.add_widget(label)
            label = Label(text="Description")
            label.size_hint_y = None
            mylayout.add_widget(label)
            label = Label(text="Points")
            label.size_hint_y = None
            mylayout.add_widget(label)
            if assignments:
                for ann in assignments:
                    label = Label(text=str(ann.assignmentName + "\n" + str(ann.assignmentDue)))
                    label.size_hint_y = None
                    mylayout.add_widget(label)
                    label = Label(text=str(ann.assignmentDesc))
                    label.size_hint_y = None
                    mylayout.add_widget(label)
                    label = Label(text=str(ann.assignmentPoints))
                    label.size_hint_y = None
                    mylayout.add_widget(label)
            else:
                label = Label(text='There are no assignments')
                label.size_hint_y = None
                mylayout.add_widget(label)
            close = Button(text='OK')
            close.size_hint_y = None
            close.bind(on_press=msg.dismiss)
            mylayout.add_widget(close)
        else:
            self.manager.current = 'DB'

    # This method creates a popup with the list of people
    def displayPeople(self):
        global coursenum
        if coursenum != 0:
            students = repo.getAllStudentsinaCourse(coursenum)
            student_nos = len(students)
            mylayout = GridLayout(cols = 3)
            msg = Popup(title='People in the course',content=mylayout)
            msg.open()
            label = Label(text="# People")
            label.size_hint_y = None
            mylayout.add_widget(label)
            label = Label(text=str(student_nos))
            label.size_hint_y = None
            mylayout.add_widget(label)
            label = Label(text="")
            label.size_hint_y = None
            mylayout.add_widget(label)
            label = Label(text="Name")
            label.size_hint_y = None
            mylayout.add_widget(label)
            label = Label(text="Username")
            label.size_hint_y = None
            mylayout.add_widget(label)
            label = Label(text="Role")
            label.size_hint_y = None
            mylayout.add_widget(label)
            if students:
                for stu in students:
                    label = Label(text=stu.name)
                    label.size_hint_y = None
                    mylayout.add_widget(label)
                    label = Label(text=stu.username)
                    label.size_hint_y = None
                    mylayout.add_widget(label)
                    label = Label(text=stu.rolename)
                    label.size_hint_y = None
                    mylayout.add_widget(label)
            else:
                label = Label(text='There are no students')
                label.size_hint_y = None
                mylayout.add_widget(label)
            close = Button(text='OK')
            close.size_hint_y = None
            close.bind(on_press=msg.dismiss)
            mylayout.add_widget(close)
        else:
            self.manager.current = 'DB'

    # This method creates a popup with the list of grades for the assignments
    def displayGrades(self):
        global coursenum,user
        if user and coursenum != 0:
            grades = repo.getAllGradesForStudent(user,coursenum)
            mylayout = GridLayout(cols = 2)
            msg = Popup(title='Grades for the course',content=mylayout)
            msg.open()
            if grades:
                label = Label(text="Assignment")
                label.size_hint_y = None
                mylayout.add_widget(label)
                label = Label(text="Grade")
                label.size_hint_y = None
                mylayout.add_widget(label)
                for grade in grades:
                    label = Label(text=grade.assignment)
                    label.size_hint_y = None
                    mylayout.add_widget(label)
                    label = Label(text=str(float(grade.points)))
                    label.size_hint_y = None
                    mylayout.add_widget(label)
            else:
                label = Label(text="No assignments are graded")
                label.size_hint_y = None
                mylayout.add_widget(label)
                label = Label(text="")
                label.size_hint_y = None
                mylayout.add_widget(label)
            close = Button(text='OK')
            close.size_hint_y = None
            close.bind(on_press=msg.dismiss)
            mylayout.add_widget(close)
        else:
            self.manager.current = 'DB'

# This function is the button action for the announcement screen
def addAnnouncement(instance):
    global sm
    if instance.text == 'Back':
        sm.current = 'courseadmin'
    else:
        sm.current = 'newann'

# This function is the button action for the assignment screen
def addAssignment(instance):
    global sm
    if instance.text == 'Back':
        sm.current = 'courseadmin'
    else:
        sm.current = 'newassignment'

class NewAnnouncementScreen(Screen):
    '''This class is a screen for new announcements'''

    # This method clears the screen of the previous information
    def clear(self):
        self.ids['name'].text = ''
        self.ids['annmsg'].text = ''

    # This method adds the new announcement to the course
    def newAnnouncement(self):
        title = self.ids['name'].text
        msg = self.ids['annmsg'].text
        res = repo.addAnnouncement(title,msg,coursenum)
        if res:
            self.manager.current = 'ann'
        else:
            self.manager.get_screen('courseadmin').ids['msg'].text = 'Could not create announcement'
            self.manager.current = 'courseadmin'

class NewAssignmentScreen(Screen):
    '''This class is a screen for new announcements'''

    # This method clears the screen of the previous information
    def clear(self):
        self.ids['name'].text = ''
        self.ids['desc'].text = ''
        self.ids['points'].text = ''
        self.ids['due'].text = ''

    # This method adds the new assignment to the course
    def newAssignment(self):
        global coursenum
        name = self.ids['name'].text
        desc = self.ids['desc'].text
        points = self.ids['points'].text
        dueDate = self.ids['due'].text

        newAssignment = Assignment()
        newAssignment.assignmentCourse = coursenum
        newAssignment.assignmentName = name
        newAssignment.assignmentDesc = desc
        newAssignment.assignmentPoints = points
        newAssignment.assignmentDue = dueDate

        res = repo.addAssignment(newAssignment)
        if res:
            self.manager.current = 'assignment'
        else:
            self.manager.get_screen('courseadmin').ids['msg'].text = 'Could not create assignment'
            self.manager.current = 'courseadmin'

class AnnouncementScreen(Screen):
    '''This class is a screen for all admin announcements'''

    # This method clears the screen of the previous information
    def clear(self):
        mylayout = self.ids["mylayout"]
        mylayout.clear_widgets()

    # This method displays all the announcements for the course
    def getAllAnnouncement(self):
        global coursenum
        global user, sm
        if coursenum != 0:
            announcements = repo.getAnnouncementsbyCourse(coursenum)
            mylayout = self.ids['mylayout']
            sm = self.manager
            if announcements:
                for ann in announcements:
                    label = Label(text=str(ann.announcementName + "\n" + str(ann.announcementDate)))
                    label.size_hint_y = None
                    mylayout.add_widget(label)
                    label = Label(text=str(ann.message))
                    label.size_hint_y = None
                    mylayout.add_widget(label)
            else:
                label = Label(text='There are no announcements')
                label.size_hint_y = None
                mylayout.add_widget(label)
            add = Button(text='ADD')
            add.size_hint_y = None
            add.bind(on_press=addAnnouncement)
            mylayout.add_widget(add)
            back = Button(text='Back')
            back.size_hint_y = None
            back.bind(on_press=addAnnouncement)
            mylayout.add_widget(back)
        else:
            self.manager.current = 'courseadmin'


class AssignmentScreen(Screen):
    '''This class is screen for all admin course assignments'''

    # This method clears the screen of the previous information
    def clear(self):
        mylayout = self.ids["mylayout"]
        mylayout.clear_widgets()

    # This method displays all the assignments for the course
    def getAllAssignment(self):
        global coursenum
        global user, sm
        if coursenum != 0:
            assignments = repo.getAssignmentsbyCourse(coursenum)
            mylayout = self.ids['mylayout']
            sm = self.manager
            if assignments:
                for ann in assignments:
                    label = Label(text=str(ann.assignmentName + "\n" + str(ann.assignmentDue)))
                    label.size_hint_y = None
                    mylayout.add_widget(label)
                    label = Label(text=str(ann.assignmentDesc))
                    label.size_hint_y = None
                    mylayout.add_widget(label)
                    label = Label(text=str(ann.assignmentPoints))
                    label.size_hint_y = None
                    mylayout.add_widget(label)
            else:
                label = Label(text='There are no assignments')
                label.size_hint_y = None
                mylayout.add_widget(label)
            add = Button(text='ADD')
            add.size_hint_y = None
            add.bind(on_press=addAssignment)
            mylayout.add_widget(add)
            back = Button(text='Back')
            back.size_hint_y = None
            back.bind(on_press=addAssignment)
            mylayout.add_widget(back)
        else:
            self.manager.current = 'courseadmin'

# This function is the button action for the people screen
def addPeople(instance):
    global sm
    if instance.text == 'Back':
        sm.current = 'courseadmin'
    elif instance.text == 'Add Existing Students':
        sm.current = 'addexistingpeople'
    elif instance.text == 'Add New Students':
        sm.current = 'newpeople'

class PeopleScreen(Screen):
    '''This class is screen for all course students'''

    # This method clears the screen of the previous information
    def clear(self):
        mylayout = self.ids["mylayout"]
        mylayout.clear_widgets()

    # This method displays all the people for the course
    def displayPeople(self):
        global coursenum
        if coursenum != 0:
            student_nos = 0
            students = repo.getAllStudentsinaCourse(coursenum)
            mylayout = self.ids['mylayout']
            if students:
                student_nos = len(students)
                label = Label(text="# People")
                label.size_hint_y = None
                mylayout.add_widget(label)
                label = Label(text=str(student_nos))
                label.size_hint_y = None
                mylayout.add_widget(label)
                label = Label(text="")
                label.size_hint_y = None
                mylayout.add_widget(label)
                label = Label(text="Name")
                label.size_hint_y = None
                mylayout.add_widget(label)
                label = Label(text="Username")
                label.size_hint_y = None
                mylayout.add_widget(label)
                label = Label(text="Role")
                label.size_hint_y = None
                mylayout.add_widget(label)
                for stu in students:
                    label = Label(text=stu.name)
                    label.size_hint_y = None
                    mylayout.add_widget(label)
                    label = Label(text=stu.username)
                    label.size_hint_y = None
                    mylayout.add_widget(label)
                    label = Label(text=stu.rolename)
                    label.size_hint_y = None
                    mylayout.add_widget(label)
                add = Button(text='Add New Students')
                add.size_hint_y = None
                add.bind(on_press=addPeople)
                mylayout.add_widget(add)
                add = Button(text='Add Existing Students')
                add.size_hint_y = None
                add.bind(on_press=addPeople)
                mylayout.add_widget(add)
                back = Button(text='Back')
                back.size_hint_y = None
                back.bind(on_press=addPeople)
                mylayout.add_widget(back)
            else:
                label = Label(text="There are no people in this class")
                label.size_hint_y = None
                mylayout.add_widget(label)
        else:
            self.manager.current = 'DB'

class NewPeopleScreen(Screen):
    '''This class is screen for all new people addition'''

    # This method clears the screen of the previous information
    def clear(self):
        self.ids['name'].text = ''
        self.ids['username'].text = ''
        if self.ids['pwd'].text != 'student100':
            self.ids['pwd'].text = 'student100'

    # This method adds new people to the course
    def newPeople(self):
        global coursenum
        name = self.ids['name'].text
        username = self.ids['username'].text
        password = self.ids['pwd'].text

        newPeople = User()
        newPeople.username = username
        newPeople.name = name
        newPeople.password = password

        res = repo.addNewStudent(newPeople,200,coursenum)
        if res:
            self.manager.current = 'people'
        else:
            self.manager.get_screen('courseadmin').ids['msg'].text = 'Could not create assignment'
            self.manager.current = 'courseadmin'

class ExisitingPeopleScreen(Screen):
    '''This class is screen for all existing people addition to the course'''

    # This method clears the screen of the previous information
    def clear(self):
        self.ids['username'].text = ''

    # This method adds existing people to the course
    def addexistingPeople(self):
        global coursenum
        username = self.ids['username'].text

        addPeople = repo.getUser(username)

        if addPeople:
            res = repo.addExistingStudent(addPeople,coursenum)
            if res:
                self.manager.current = 'people'
            else:
                self.manager.get_screen('courseadmin').ids['msg'].text = 'Could not create assignment'
                self.manager.current = 'courseadmin'

class CourseScreenAdmin(Screen):
    '''
    This is the screen to display various options for each course for an ADMIN
    '''

    # This method clears the screen of the previous information
    def clear(self):
        self.ids['msg'].text = ''

    # This method sets the initial data for the screen
    def initial(self):
        global user, coursenum
        coursename = repo.getCourseByCoursenum(coursenum)
        self.ids['info'].text = 'Welcome ' + user.username + " to " + coursename

def displaycourse(instance):
    '''
    This is the method for the onpress event for the button on dashboard
    :param instance:
    :return:
    '''
    global coursenum
    global user
    coursenum = int(instance.text)
    if user.rolename == 'student':
        sm.current = "coursestu"
    else:
        sm.current = "courseadmin"

def logout(instance):
    '''
    This is the method for the onpress event for the logout button on dashboard
    :param instance:
    :return:
    '''
    global user
    user = None
    sm.current = "home"

class ChangePassword(Screen):
    '''
    This class is the screen to change the password
    '''

    # This method clears the screen of the previous information
    def clear(self):
        newpass = self.ids["newpass"]
        newpass.text = ''
        self.ids['msg'].text = ''

    # This method clears the screen
    def change(self):
        global user
        newpass = self.ids["newpass"].text
        res = repo.changePassword(user.username,newpass)
        if res:
            self.ids["msg"].text = 'Password Changed'
        else:
            self.ids["msg"].text = 'Password could not be changed'

class DashBoardScreen(Screen):
    '''
    This screen displays the list of courses
    '''

    # This method clears the screen of the previous information
    def clear(self):
        mylayout = self.ids["mylayout"]
        mylayout.clear_widgets()

    # This method changes the current screen to the password screen
    def changepass(self,instance):
        sm.current = 'pwd'

    # This method retrieves all the courses for the given user
    def getCourses(self):
        global courses
        global sm
        global user
        if user:
            courses = repo.getAllCoursesForStudent(user)
            mylayout = self.ids["mylayout"]
            sm = self.manager
            label = Label(text='Welcome ')
            label.size_hint_y = None
            mylayout.add_widget(label)
            label = Label(text=str(user.username))
            label.size_hint_y = None
            mylayout.add_widget(label)
            if courses:
                for course in courses: # For each course add the course details as list to the screen
                    label = Label(text=str(course.coursename))
                    label.size_hint_y = None
                    mylayout.add_widget(label)
                    button = Button(text=str(course.coursenum))
                    button.bind(on_press=displaycourse)
                    button.size_hint_y = None
                    mylayout.add_widget(button)
            else:
                label = Label(text='There are no courses')
                label.size_hint_y = None
                mylayout.add_widget(label)
            logoutbtn = Button(text="Logout")
            logoutbtn.bind(on_press=logout)
            logoutbtn.size_hint_y = None
            mylayout.add_widget(logoutbtn)
            changepwd = Button(text="Change Password")
            changepwd.bind(on_press=self.changepass)
            changepwd.size_hint_y = None
            mylayout.add_widget(changepwd)
        else:
            self.manager.current = "login"

class LoginScreen(Screen):
    '''
    This is the screen to login to the canvas application
    '''

    # This method clears the screen of the previous information
    def clear(self):
        self.ids['username'].text = ""
        self.ids['password'].text = ""
        self.ids['msg'].text = ''

    # This method clears the screen and redirects the current screen back to home screen
    def onLogout(self):
        self.ids['username'].text = ""
        self.ids['password'].text = ""
        self.manager.current = "home"

    # This method redirects to the current screen to the Dash Board for all valid users
    def onLogin(self):
        username = self.ids['username'].text
        password = self.ids['password'].text
        res = repo.verifyUser(username,password)
        if res:
            global user
            user = res
            self.manager.current = "DB"
        else:
            self.ids['msg'].text = "Invalid User"

class FileScreen(Screen):
    '''
    This class is the screen to add new files to the course
    '''
    filefullpath = ''
    filename = ''

    # This method is called on selecting a file from the file chooser
    def selectFile(self):
        self.filefullpath = self.ids["fc"].selection[0]
        filepaths = self.filefullpath.split('/')
        filepaths.reverse()
        self.filename = filepaths[0]

    # This method is called when the 'ADD' button is clicked
    def saveFile(self):
        global coursenum
        if coursenum:
            file = Files()
            file.fileName = self.filename
            file.filePath = self.filefullpath
            res = repo.addFile(file,coursenum)
            if res > 0:
                self.manager.get_screen('courseadmin').ids['msg'].text = 'File Added'
            else:
                self.manager.get_screen('courseadmin').ids['msg'].text = 'File could not be added'
        else:
            self.manager.get_screen('courseadmin').ids['msg'].text = 'Invalid course'
        self.manager.current = 'courseadmin'

class FileScreenDisplay(Screen):
    '''
    This class is the screen to display all the files in the course
    '''
    role = ''

    # This method clears the screen of the previous information
    def clear(self):
        mylayout = self.ids["mylayout"]
        mylayout.clear_widgets()

    # This method is called when the download button is clicked - it downloads the file to the user's Download directory
    def downloadFile(self, instance):
        file = repo.getFilebyId(instance.text)
        content = None
        mainPath = '/Users/anitageorge/Downloads/'
        with open(file.filePath, 'rb') as f:
            content = f.read()

        if content:
            with open(mainPath + file.fileName, 'wb') as f2:
                f2.write(content)
                self.manager.get_screen(self.role).ids['msg'].text = 'File downloaded'
        else:
            self.manager.get_screen(self.role).ids['msg'].text = 'File could not be downloaded'
        self.manager.current = self.role

    # This method redirects the screen to the admin or student screen based on user role
    def close(self, instance):
        self.manager.current = self.role

    # This method redirects the screen to the file screen to add a new file
    def addFile(self, instance):
        self.manager.current = 'file'

    # This method displays all the files of the course
    def displayFiles(self):
        global coursenum, user
        if user.rolename == 'admin':
            self.role = 'courseadmin'
        else:
            self.role = 'coursestu'
        if coursenum != 0:
            files = repo.getAllFilesForCourse(coursenum)
            mylayout = self.ids['mylayout']
            if files:
                label = Label(text='Click on the FileID to download')
                label.size_hint_y = None
                mylayout.add_widget(label)
                label = Label(text='')
                label.size_hint_y = None
                mylayout.add_widget(label)
                for fi in files:
                    label = Label(text=str(fi.fileName))
                    label.size_hint_y = None
                    mylayout.add_widget(label)
                    savebtn = Button(text=str(fi.fileId))
                    savebtn.size_hint_y = None
                    savebtn.bind(on_press=self.downloadFile)
                    mylayout.add_widget(savebtn)
            else:
                label = Label(text='There are no files for this course yet')
                label.size_hint_y = None
                mylayout.add_widget(label)
                label = Label(text='')
                label.size_hint_y = None
                mylayout.add_widget(label)
            if user.rolename == 'admin':
                add = Button(text='Add Files')
                add.size_hint_y = None
                add.bind(on_press=self.addFile)
                mylayout.add_widget(add)
            close = Button(text='Back')
            close.size_hint_y = None
            close.bind(on_press=self.close)
            mylayout.add_widget(close)
        else:
            self.manager.current = self.role

class GradesScreen(Screen):
    '''
    This class is the screen to display all student grades
    '''
    assignmentID = 0
    newids = []

    # This method redirects the screen to the admin screen
    def close(self,instance):
        if instance.text == 'Back':
            self.manager.current = 'courseadmin'

    # This method clears the screen of the previous information
    def clear(self):
        mylayout = self.ids["mylayout"]
        mylayout.clear_widgets()

    # This method submits the grade for each student for an assignment
    def submitgrades(self,instance):
        btnname = instance.id
        btnname = btnname.replace('btn','')
        username = ''
        points = 0
        global coursenum
        msg = None
        for nid in self.newids:
            if nid.id == 'msg':
                msg = nid
        for nid in self.newids:
            if nid.id == btnname + "lbl":
                username = nid.text
            if nid.id == btnname + "txt":
                points = float(nid.text)
                res = repo.addStudentGrade(username,coursenum, self.assignmentID,points)
                if res and res < 1:
                    msg.text = 'Grade not Added'
                elif res and res > 0:
                    msg.text = 'Grade submitted for ' + username
                else:
                    msg.text = 'Grade not Added'

    # This method displays all the grades for all students for an assignment
    def listgrades(self,instance):
        self.clear()
        mylayout = self.ids['mylayout']
        mylayout.cols = 3
        self.assignmentID = int(instance.text)
        global coursenum
        grades = repo.getGradesForAssignment(coursenum,self.assignmentID)
        if grades:
            label = Label(text='Student Username')
            label.size_hint_y = None
            mylayout.add_widget(label)
            label = Label(text='GradePoint for ' + str(self.assignmentID))
            label.size_hint_y = None
            mylayout.add_widget(label)
            label = Label(text='')
            label.id = 'msg'
            label.size_hint_y = None
            self.newids.append(label)
            mylayout.add_widget(label)
            for grade in grades:
                label = Label(text=grade.username)
                label.size_hint_y = None
                label.id = grade.username + 'lbl'
                self.newids.append(label)
                mylayout.add_widget(label)
                text = TextInput(text=str(grade.point))
                text.size_hint_y = None
                text.id = grade.username + 'txt'
                self.newids.append(text)
                mylayout.add_widget(text)
                gradebtn = Button(text='Submit')
                gradebtn.id = grade.username + 'btn'
                gradebtn.size_hint_y = None
                gradebtn.bind(on_press=self.submitgrades)
                mylayout.add_widget(gradebtn)
            close = Button(text='Back')
            close.size_hint_y = None
            close.bind(on_press=self.close)
            mylayout.add_widget(close)

    # This method displays all the assignments in the course
    def displayAssignments(self):
        global coursenum
        if coursenum:
            assignments = repo.getAssignmentsbyCourse(coursenum)
            mylayout = self.ids['mylayout']
            mylayout.cols = 2
            if assignments:
                label = Label(text='Click on the Assignment ID to view or change grades')
                label.size_hint_y = None
                mylayout.add_widget(label)
                label = Label(text='')
                label.size_hint_y = None
                mylayout.add_widget(label)
                for assignment in assignments:
                    label = Label(text=str(assignment.assignmentName))
                    label.size_hint_y = None
                    mylayout.add_widget(label)
                    gradebtn = Button(text=str(assignment.assignmentID))
                    gradebtn.size_hint_y = None
                    gradebtn.bind(on_press=self.listgrades)
                    mylayout.add_widget(gradebtn)
            else:
                label = Label(text='There are no assignments for this course')
                label.size_hint_y = None
                mylayout.add_widget(label)
                label = Label(text='')
                label.size_hint_y = None
                mylayout.add_widget(label)
            close = Button(text='Back')
            close.size_hint_y = None
            close.bind(on_press=self.close)
            mylayout.add_widget(close)
        else:
            self.manager.current = 'DB'

class ScreenManagement(ScreenManager):
    '''
    This class is the screenManager to move between various screens
    '''
    pass

class MainApp(App):
    '''
    This is the root of the canvas application
    '''
    def build(self):
        return super().build()

if __name__ == '__main__':
    MainApp().run()
