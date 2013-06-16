import sqlite3
_connection = None

### TABLES ###
# users
# students
# nominees
# nominators
# nominee_fields
# voters
# votes

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
	if 'nominee_fields' not in table_names:
		create_nominee_fields_table(cursor)
	if 'nominators' not in table_names:
		create_nominators_table(cursor)
	if 'voters' not in table_names:
		create_voters_table(cursor)
	if 'votes' not in table_names:
		create_votes_table(cursor)

	connection.commit()
	
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
	print "INFO: Creating nominees table"
	cursor.execute("""
create table nominees
(
userid integer primary key
);
""")

def create_nominee_fields_table(cursor):
	print "INFO: Creating nominee_fields table"
	cursor.execute("""
create table nominee_fields
(
field text,
userid integer,
submission text,
primary key (field, userid)
foreign key (userid) references nominees (userid)
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

def create_voters_table(cursor):
	print "INFO: Creating has_voted table"
	cursor.execute("""
create table voters
(
userid integer,
primary key (userid),
foreign key (userid) references users (userid)
);
""")

def create_votes_table(cursor):
	print "INFO: Creating voted table"
	cursor.execute("""
create table votes
(
userid integer,
voted integer,
primary key (userid, voted),
foreign key (userid) references voters (userid),
foreign key (voted) references nominees (userid)
);
""")
