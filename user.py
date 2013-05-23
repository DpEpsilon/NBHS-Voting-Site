import sqlite3
import databse_engine

class User(object):
	def __init__(self, userid, password, firstname, lastname,\
					 student_info=None, nominee_info=None):
		self.userid = userid
		self.password = password
		self.firstname = firstname
		self.lastname = lastname
		self.student_info = student_info
		self.nominee_info = nominee_info

class StudentInfo(object):
	def __init__(self, year, house):
		self.year = year
		self.house = house

class NomineeInfo(object):
	def __init__(self, experience, why):
		self.experience = experience
		self.why = why

