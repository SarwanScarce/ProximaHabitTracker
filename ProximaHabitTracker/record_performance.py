# Used to import datetime class
from datetime import datetime
# SQLite3 used to create a database
import sqlite3
# Used to import pandas as pd
import pandas as pd
# Used to import tabulate from tabulate
from tabulate import tabulate
# Used to import check_streak from check_streak
from check_streak import check_streak
# Used to import check_periodicity from check_periodicity
from check_periodicity import check_periodicity


# # Used to create the connection to the database
# conn = sqlite3.connect('habits_database.db')
# c = conn.cursor()
#
#
# # Used to create a table in the database, commented out after use
# # Specification requires a description of the habit that will remind the user what he/she has to do before checking off this habit
# # Periodicity relates to whether the habit is done on a daily or weekly basis
# sql = """CREATE TABLE "performance_table" (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             habitName TEXT NOT NULL,
#             dateCreated TEXT NOT NULL,
#             week_of_the_year INTEGER TEXT NOT NULL,
#             streak_maintained TEXT NOT NULL,
#             periodicity TEXT NOT NULL);"""
#
# sql = "ALTER TABLE performance_table ADD week_of_the_year"
#
#
# sql = "ALTER TABLE performance_table ADD streak_maintained"
#
#
# sql = "ALTER TABLE performance_table ADD periodicity"
#
#
# c.execute(sql)
# conn.commit()
# print("Table Created")
# c.close()


# Used to create the new_record() function
def new_record():

    print('\n')

    # Used to create the connection to the database
    conn = sqlite3.connect('habits_database.db')
    # Used to create cursor object
    c = conn.cursor()

    # Used to output the user_habits table
    c.execute("SELECT habitName, specification, periodicity FROM habits_table")
    my_data = [c]
    for x in my_data:
        df = pd.DataFrame(x)
        print(tabulate(df, headers=["Habit Name", "Specification", "Periodicity", "Date Created"], tablefmt='psql'))

    # Used to prompt the user to provide the name of the habit
    habit_name = input('Enter the name of the habit you would like to check off: ')

    # This variable is created to record the date the habit was checked off
    date_today = datetime.today().strftime('%Y-%m-%d')

    # This variable is created to record the week of the year the habit was checked off
    week_of_the_year = datetime.today().strftime('%V')

    # This variable calls on the check_streak() function to determine and record if the streak was maintained for the habit being checked off
    streak_maintained = check_streak(habit_name)

    # This variable calls on the check_periodicity() function to determine and record the periodicity of the habit being checked off
    periodicity = check_periodicity(habit_name)

    # The habit entered by the user that they wish to check off is checked against the habits_table
    c.execute("SELECT * FROM habits_table WHERE habitName ='{}'".format(habit_name))

    # If it exists then the record is inserted into the performance_table
    if c.fetchall():

        # Used to insert new habit into the performance_table table
        c.execute("""INSERT INTO performance_table
            (habitName, periodicity, dateCreated, week_of_the_year, streak_maintained)
            VALUES ('{}','{}','{}','{}','{}');""".format (habit_name, periodicity, date_today, week_of_the_year, streak_maintained))

        # Informs the user that the habit is added
        print("\nRecord Added")

        # The user clicks the run button to carry out another action
        print("Click Rerun to continue")

    # If it does not exist this action is executed
    else:
        # If the habit entered does not exist, the user is prompted to enter one that does exist to proceed
        print('You can only checkoff existing habits. Please select one!')

        # The user clicks the run button to carry out another action
        print("Click Rerun to continue")

    conn.commit()