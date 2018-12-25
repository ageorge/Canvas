'''
This file contains model classes related to a user as per database or screen design
1. user
2. role
3. userrole
'''

class User:
    def __init__(self, user = None):
        if user:
            self.username = str(user[0])
            self.name = str(user[1])
            self.password = str(user[2])
            self.rolename = str(user[3])
        else:
            self.username = ''
            self.name = ''
            self.password = ''
            self.rolename = ''

    def __str__(self):
        s = self.username + " | " + self.name + " | " + self.rolename + " | " + self.password
        return s

class Role:
    def __init__(self, roleid, rolename):
        self.roleid = roleid
        self.rolename = rolename

class UserRole:
    def __init__(self, username, rolename):
        self.username = username
        self.rolename = rolename
