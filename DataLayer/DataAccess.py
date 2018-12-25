import pymysql
from contextlib import closing
import logging

class DataAccess:
    '''
    This class connects to the database and returns the appropriate result
    Database used = MySql
    Database name = canvas
    '''
    def __init__(self):
        self.conn = pymysql.connect(host="localhost", user="root", password="root", database="canvas")  # Connection object to connect to mysql database

    '''
    This method is used to execute only select statement 
    Returns a list of objects
    '''
    def executeSelectStatement(self,query,params = None):
        try:
            with closing(self.conn.cursor()) as c:
                c.execute(query,params)
                result = c.fetchall()
                if len(result) > 0:
                    return result
                else:
                    return None
        except Exception as e:
            logging.error(e)

    '''
    This method is used to execute insert, update and delete statements
    Returns True if number of rows modified is greater than 1
    else returns False
    '''
    def executeInsertUpdateDelete(self,query,params = None):
        try:
            with closing(self.conn.cursor()) as c:
                c.execute(query,params)
                self.conn.commit()
                if c.rowcount > 0:
                    return True
                else:
                    return False
        except Exception as e:
            logging.error(e)
