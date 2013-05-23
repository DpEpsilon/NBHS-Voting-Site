import sqlite3
from database_engine import get_db_connection

import hashlib

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

def hash_password(password):
	# sha512 may be overkill
    return hashlib.sha512(password).hexdigest()
		
def get_user(user):
	"""
	Takes a userid or username.
	Returns the user to which the userid or username corresponds.
	"""
	if user is None:
		return None
		
	connection = get_db_connection()
	cursor = connection.cursor()
	if type(user) == int:
		cursor.execute("select userid, username, password, firstname, lastname "
					   "from users where userid = ?", (user,))
	elif isinstance(user, basestring):
		cursor.execute("select userid, username, password, firstname, lastname "
					   "from users where username = ?", (user,))
	else:
		raise TypeError("user argument passed to get_user must "
						"be and integer or a string or None.")

	user_table_row = cursor.fetchone()
	if user_table_row is None:
		return None

	userid = user_table_row[0]
	
	cursor.execute("select year, house from students "
				   "where userid = ?", (userid,))
	student_table_row = cursor.fetchone()
	cursor.execute("select experience, why from nominees "
				   "where userid = ?", (userid,))
	nominees_table_row = cursor.fetchone()

	return User(user_table_row[0],
				user_table_row[1],
				user_table_row[2],
				user_table_row[3],
				StudentInfo(student_table_row[0],
							student_table_row[1]),
				NomineeInfo(nominees_table_row[0],
							nominees_table_row[1]))

def is_valid_login(username, password):
	"""
	Checks if a username, password pair match.
	Returns 0 if they do, 1 if pass doesn't match, 2 if username doesn't exist
	"""
	connection = get_db_connection()
	cursor = connection.cursor()

	username = username.lower() # Case insensitivity.
	
	query = cursor.execute("""SELECT password FROM users WHERE username = ?""", (username,)).fetchone()

	if not query:
		return 2
	if query[0] == hash_password(password):
		return 0
	else:
		return 1
