import sqlite3
import database_engine

def add_nominee_field(userid, field, submission):
	connection = database_engine.get_db_connection()
	cursor = connection.cursor()

	cursor.execute("""insert into nominee_fields (userid, field, submission)
values (?, ?, ?);""", (userid, field, submission))