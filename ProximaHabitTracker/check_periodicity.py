# SQLite3 used to create a database
import sqlite3


# Used to create the check_periodicity() function
def check_periodicity(habit_name):

    # Used to create the connection to the database
    conn = sqlite3.connect('habits_database.db')
    # Used to create cursor object
    c = conn.cursor()

    # Used to create a table from the habits_table using the habit name inputted to determine whether a habit is daly or weekly
    c.execute("SELECT periodicity FROM habits_table WHERE habitName=?", (habit_name,))
    periodicity1 = c.fetchone()
    periodicity = "".join(periodicity1[0])
    if (periodicity == 'Weekly'):
        return('Weekly')
    else:
        return('Daily')

