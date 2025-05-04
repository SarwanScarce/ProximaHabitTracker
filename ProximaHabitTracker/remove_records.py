# SQLite3 used to create a database
import sqlite3
# Used to import pandas as pd
import pandas as pd
# Used to import tabulate from tabulate
from tabulate import tabulate


# Used to create the remove_a_habit() function
def remove_a_habit():

    print('\n')

    # Used to create the connection to the database
    conn = sqlite3.connect('habits_database.db')
    # Used to create cursor object
    c = conn.cursor()

    # Used to output the habits_table table
    c.execute("SELECT habitName, specification, periodicity FROM habits_table")
    my_data = [c]
    for x in my_data:
        df = pd.DataFrame(x)
        print(tabulate(df, headers=["Habit Name", "Specification", "Periodicity", "Date Created"], tablefmt='psql'))

    # Used to prompt the user to provide the name of the habit and related records they would like to remove
    habit_name = input('Enter the name of the habit you would like to remove: ')

    # The habit entered by the user that they wish to check off is checked against the habits_table
    c.execute("SELECT * FROM habits_table WHERE habitName ='{}'".format(habit_name))

    # If it exists then the following action is taken
    if c.fetchall():

        # Used to delete chosen habit from the habits_table table
        c.execute("""DELETE FROM habits_table WHERE habitName =?""", (habit_name,))

        # Used to delete the records of the chosen habit from the performance_table table
        c.execute("""DELETE FROM performance_table WHERE habitName =?""", (habit_name,))

        # Informs the user that the habit and the related records was deleted
        print("\nRecord Deleted")

        # The user clicks the run button to carry out another action
        print("Click Rerun to continue")

    else:
        # If the habit entered does not exist, the user is prompted to enter one that does exist to proceed
        print('You can only delete existing habits. Please select one!')

        # The user clicks the run button to carry out another action
        print("Click Rerun to continue")

    conn.commit()
