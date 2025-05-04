# Used to import datetime from datetime class
from datetime import datetime
# SQLite3 used to create a database
import sqlite3


# Used to create the connection to the database
conn = sqlite3.connect('habits_database.db')
# Used to create cursor object
c = conn.cursor()

# # Used to create a table in the database, commented out after use
# # Specification requires a description of the habit that will remind the user what he/she has to do before checking off this habit
# # Periodicity relates to whether the habit is done on a daily or weekly basis
# c.execute("""CREATE TABLE "habits_table" (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             habitName TEXT NOT NULL,
#             specification TEXT NOT NULL,
#             periodicity TEXT NOT NULL,
#             dateCreated TEXT NOT NULL);""")
#
#
# c.execute("""CREATE VIEW user_habits AS
#     SELECT habitName, specification, periodicity FROM habits_table""")
#
# conn.commit()


# Used to create the new_habit() function
def new_habit():

    # Used to prompt the user to provide the name of the habit
    habit_name = input('\nHabit Name: ')

    # Used to find check that the habit entered does not exist
    # If the habit does not exist then a new habit is created
    c.execute("SELECT * FROM habits_table WHERE habitName ='{}'".format(habit_name))
    if c.fetchall():
        print('This habit already exists. Please enter new habit.')
        print("Click Rerun to continue")
    else:
        # Used to prompt the user to provide a description/activities that must be completed before this habit is checked off
        description = input('\nActivities that must be completed before checkoff: ')

        # This variable is created to record the date the habit was created
        date_created = datetime.today().strftime('%Y-%m-%d')

        # Used to prompt the user to specify if this is a daily or weekly habit
        basis = input('\nDaily or weekly habit: ')
        if (basis == 'Weekly'):
            periodicity = 'Weekly'

            # Used to insert new habit into the table
            c.execute("""INSERT INTO habits_table
                (habitName, specification, periodicity, dateCreated)
                VALUES ('{}','{}','{}', '{}');""".format(habit_name, description, periodicity, date_created))

            print("\nHabits Updated")

        elif (basis == 'Daily'):
            periodicity = 'Daily'

            # Used to insert new habit into the table
            c.execute("""INSERT INTO habits_table
                (habitName, specification, periodicity, dateCreated)
                VALUES ('{}','{}','{}', '{}');""".format(habit_name, description, periodicity, date_created))

            print("\nHabits Updated")

        else:
            # If the user does not choose Daily and Weekly then they are prompted to do so
            print('Choose Daily or Weekly')
            # The user clicks the run button to carry out another action
            print("Click Rerun to continue")

    conn.commit()
    c.close()



