import sqlite3
import database_engine

def add_nominee(userid):
	connection = database_engine.get_db_connection()
	cursor = connection.cursor()
	cursor.execute("""insert into nominees (userid) values (?)""",
				   (userid,))
	connection.commit()

def add_nominee_field(userid, field, submission):
	connection = database_engine.get_db_connection()
	cursor = connection.cursor()

	cursor.execute("""insert into nominee_fields (userid, field, submission)
values (?, ?, ?);""", (userid, field, submission))
	connection.commit()

def delete_nominee_field(userid, field):
	connection = database_engine.get_db_connection()
	cursor = connection.cursor()
	cursor.execute("""select submission from nominee_fields
 where userid = ? and field = ?""", (userid, field))

	old_submission = cursor.fetchone()
	if old_submission is not None:
		deletelog = open('deletelog.txt', 'a')
		deletelog.write(str(userid) + ',' + field + ':\n' +
						repr(old_submission[0]) + '\n')
		del deletelog
	
	cursor.execute("""delete from nominee_fields
 where userid = ? and field = ?""", (userid, field))
	connection.commit()
	
