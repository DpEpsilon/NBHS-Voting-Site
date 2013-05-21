import sqlite3
_connection = None

### TABLES ###
# users
# students
# nominees
# nominators

def get_db_connection():
	global _connection
	if not _connection:
		_connection = sqlite3.Connection('sitedatabase.db')
	return _connection

def init_db():
	connection = get_db_connection()
	cursor = connection.cursor()
	cursor.execute("select * from sqlite_master WHERE type='table';")
	table_names = set()
	for entry in cursor:
		table_names.add(entry[1])

	# This can probably be done a *lot* better
	if 'users' not in table_names:
		create_users_table(cursor)
	if 'students' not in table_names:
		create_students_table(cursor)
	if 'nominees' not in table_names:
		create_nominees_table(cursor)
	if 'nominators' not in table_names:
		create_nominators_table(cursor)
	
		
	connection.close()
	
def create_users_table(cursor):
	print "INFO: Creating users table"
	cursor.execute("""
create table users
(
userid integer primary key autoincrement,
username text unique,
password text,
firstname text,
lastname text
);
""")

def create_students_table(cursor):
	print "INFO: Creating students table"
	cursor.execute("""
create table students
(
userid integer primary key,
year integer,
house text,
foreign key (userid) references users (userid)
);
""")

def create_nominees_table(cursor):
	print "INFO: Creating nominees_table"
	cursor.execute("""
create table nominees
(
userid integer primary key,
experience text,
why text,
foreign key (userid) references students (userid)
);
""")

def create_nominators_table(cursor):
	print "INFO: Creating nominators_table"
	cursor.execute("""
create table nominators
(
userid integer,
nominee integer,
why text,
primary key (userid, nominee),
foreign key (userid) references students (userid),
foreign key (nominee) references nominees (userid)
);
""")
