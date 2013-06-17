import database_engine
import user

def vote_count():

    connection = database_engine.get_db_connection()
    cursor = connection.cursor()

    nominees = {}
    for nominee in user.get_nominees():
        nominees[nominee.userid] = (0, nominee.firstname + " " + nominee.lastname)

    cursor.execute("""SELECT * FROM votes""")
    for vote in cursor.fetchall():
        voter = cursor.execute("""SELECT * FROM students WHERE userid = ?""", (vote[0],)).fetchone() # Get student who voted
        if voter is None or voter[1] == 11: # Gets 2 votes if isn't a student or is Yr11
            nominees[vote[1]] = (nominees[vote[1]][0] + 2, nominees[vote[1]][1])
        else:
            nominees[vote[1]] = (nominees[vote[1]][0] + 1, nominees[vote[1]][1])

    return nominees