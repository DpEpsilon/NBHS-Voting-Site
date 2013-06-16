import sqlite3
import database_engine

import hashlib

class User(object):
	def __init__(self, userid, username, password, firstname, lastname,\
					 student_info=None):
		self.userid = userid
		self.username = username
		self.password = password
		self.firstname = firstname
		self.lastname = lastname
		self.student_info = student_info

class StudentInfo(object):
	def __init__(self, year, house, is_nominee, nominee_fields, nominators):
		self.year = year
		self.house = house
		self.is_nominee = is_nominee
		self.nominee_fields = nominee_fields
		self.nominators = nominators

def hash_password(password):
	# sha512 may be overkill
    return hashlib.sha512(password).hexdigest()

def get_fullname(user):
	name = None
	if user is not None:
		name = user.firstname + ' ' + user.lastname
	return name

def get_nominees(year=None, house=None):
	connection = database_engine.get_db_connection()
	cursor = connection.cursor()

	condition = ""
	
	arguments = []
	if year is not None:
		arguments.append(year)
		condition += " and students.year = ?"
	if house is not None:
		arguments.append(house)
		condition += " and students.house = ?"
		
	if year is None and house is None:
		cursor.execute("select users.userid, firstname, lastname "
					   "from users join nominees, students "
					   "where nominees.userid = users.userid and "
					   "students.userid = users.userid" +
					   condition)
	
	tuples = cursor.fetchall()
	nominees = []
	for t in tuples:
		current_nominee = User(t[0], None, None, t[1], t[2],
							   get_student_info(t[0]))
		nominees.append(current_nominee)
	
	return nominees
	
def get_user(user):
	"""
	Takes a userid or username.
	Returns the user to which the userid or username corresponds.
	"""
	if user is None:
		return None
		
	connection = database_engine.get_db_connection()
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
	print user_table_row
	userid = user_table_row[0]

	student_info = get_student_info(userid)
	
	return User(user_table_row[0],
				user_table_row[1],
				user_table_row[2],
				user_table_row[3],
				user_table_row[4],
				student_info)

def get_student_info(userid):
	connection = database_engine.get_db_connection()
	cursor = connection.cursor()

	cursor.execute("select year, house from students "
				   "where userid = ?", (userid,))
	student_table_row = cursor.fetchone()

	is_nominee = get_is_nominee(userid)
	nominee_fields = get_nominee_fields(userid)
	nominators = get_nominators(userid)
	
	student_info = None
	if student_table_row is not None:
		student_info = StudentInfo(student_table_row[0],
								   student_table_row[1],
								   is_nominee,
								   nominee_fields,
								   nominators)
	return student_info


def get_is_nominee(userid):
	connection = database_engine.get_db_connection()
	cursor = connection.cursor()

	cursor.execute("select userid from nominees "
				   "where userid = ?", (userid,))
	nominees_table_row = cursor.fetchone()

	return nominees_table_row is not None

def get_nominee_fields(userid):
	connection = database_engine.get_db_connection()
	cursor = connection.cursor()
	cursor.execute("select field, submission from nominee_fields "
				   "where userid = ?", (userid,))

	return dict(cursor.fetchall())

def get_nominators(userid):
	connection = database_engine.get_db_connection()
	cursor = connection.cursor()
	cursor.execute("select userid, why from nominators "
				   "where nominee = ?", (userid,))

	return dict(cursor.fetchall())

def is_valid_login(username, password):
	"""
	Checks if a username, password pair match.
	Returns 0 if they do, 1 if pass doesn't match, 2 if username doesn't exist
	"""
	connection = database_engine.get_db_connection()
	cursor = connection.cursor()

	username = username.lower() # Case insensitivity.
	
	query = cursor.execute("""SELECT password FROM users WHERE username = ?""",
						   (username,)).fetchone()

	if not query:
		return 2
	if query[0] == hash_password(password):
		return 0
	else:
		return 1
