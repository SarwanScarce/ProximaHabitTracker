# Used to import datetime class
import datetime
# SQLite3 used to create a database
import sqlite3
# Used to import pandas as pd
import pandas as pd
# Used to import tabulate from tabulate
from tabulate import tabulate


# Used to create the track_a_habit() function
def track_a_habit():

    # Used to create the connection to the database
    conn = sqlite3.connect('habits_database.db')
    # Used to create cursor object
    c = conn.cursor()

    # Used to provide instructions
    print('\nTrack your habits by selecting one of the options below:')

    # Used to create a habit
    print('Option A: View a list of all habits')

    # to record performance
    print('Option B: View a list of habits by periodicity')

    # Used to track performance
    print('Option C: View the longest run streak for a defined habit')

    # Used to track performance
    print('Option D: View the habit with the longest run streak')

    print('\n')

    # Used to prompt the user to choose an option
    chosen_option = input('What would you like to do today?: ')

    # Executed if option 'A' is entered
    if (chosen_option == 'A'):

        # To create a view of all habits
        c.execute("""CREATE VIEW user_habits AS
            SELECT habitName, specification, periodicity FROM habits_table""")

        # Used to output user_habits view as a table
        c.execute("SELECT * FROM user_habits")
        my_data = [c]
        for x in my_data:
            df = pd.DataFrame(x)
            print(tabulate(df, headers=["No.","Habit Name", "Specification", "Periodicity"], tablefmt='psql'))

        # Used to drop the user_habits view
        c.execute("DROP VIEW user_habits")

        conn.commit()

        # The user clicks the run button to carry out another action
        print("Click Rerun to continue")
        c.close()

    # Executed if option 'B' is entered
    elif (chosen_option == 'B'):
        periodicity_choice = input('\nWould you like to track your Weekly or Daily habits? ')

        # Execute different options if 'Weekly' or 'Daily' option is selected
        if (periodicity_choice == 'Weekly'):

            # Used to create a view of all weekly habits
            c.execute("""CREATE VIEW weekly_habits AS
                SELECT habitName, specification, periodicity FROM habits_table WHERE periodicity == 'Weekly'""")

            # Used to create a table from weekly_habits
            c.execute("SELECT * FROM weekly_habits")
            my_data = [c]
            for x in my_data:
                df = pd.DataFrame(x)
                print(tabulate(df, headers=["No.","Habit Name", "Specification", "Periodicity"], tablefmt='psql'))

            # Used to drop the weekly_habits
            c.execute("DROP VIEW weekly_habits")

            conn.commit()

            # The user clicks the run button to carry out another action
            print("Click Rerun to continue")
            c.close()

        elif (periodicity_choice == 'Daily'):

            # Used to create a view of all daily habits
            c.execute("""CREATE VIEW daily_habits AS
                SELECT habitName, specification, periodicity FROM habits_table WHERE periodicity == 'Daily'""")

            # Used to create a table from daily_habits
            c.execute("SELECT * FROM daily_habits")
            my_data = [c]
            for x in my_data:
                df = pd.DataFrame(x)
                print(tabulate(df, headers=["No.","Habit Name", "Specification", "Periodicity"], tablefmt='psql'))

            # Used to drop the daily_habits
            c.execute("DROP VIEW daily_habits")

            conn.commit()
            print("Click Rerun to continue")
            c.close()

        else:
            # If the user does not choose Daily and Weekly then they are prompted to do so
            print('Choose either Weekly or Daily!')
            # The user clicks the run button to carry out another action
            print("Click Rerun to continue")

    # Executed if option 'C' is entered
    elif (chosen_option == 'C'):

        # Used to create the connection to the database
        conn = sqlite3.connect('habits_database.db')
        # Used to create cursor object
        c = conn.cursor()

        # Used to create a view of all habits
        c.execute("SELECT habitName, specification, periodicity FROM habits_table")
        my_data = [c]

        # Used to create a table of the data selected
        for x in my_data:
            df = pd.DataFrame(x)
            print(tabulate(df, headers=["No.","Habit Name", "Specification", "Periodicity"], tablefmt='psql'))

        # Used to prompt the user to provide the name of the habit
        habit_name = input('\nEnter the name of the habit you would like to see the longest run streak for: ')

        # Used to create a table of the data selected based on the habit name inputted
        sql = "SELECT * FROM habits_table WHERE habitName ='{}'".format(habit_name)
        c.execute(sql)

        # Executes if a valid habit is found
        if c.fetchall():

            # Tracking daily performance
            # Creates view "ranked" from table "performance_table"
            c.execute("""CREATE VIEW ranked AS
                SELECT habitName, dateCreated, week_of_the_year, streak_maintained, periodicity,
                ROW_NUMBER() OVER (PARTITION BY streak_maintained ORDER BY habitName) AS ranking,
                julianday(dateCreated) AS julian
                FROM performance_table   
                WHERE streak_maintained == 'Yes'""")

            # Creates view "grouped" from view "ranked"
            c.execute("""CREATE VIEW grouped AS
                SELECT *,
                    (ranking - julian) AS grouping
                FROM ranked""")

            # Creates view "grouped1" from view "grouped"
            c.execute("""CREATE VIEW grouped1 AS
                SELECT *, COUNT() AS groupCount
                FROM grouped
                GROUP BY grouping
                ORDER BY groupCount DESC""")

            # Finds the longest streak for the habit selected
            c.execute("""SELECT groupCount
                FROM grouped1
                WHERE habitName =?""", (habit_name,))
            group_count = c.fetchone()
            days_checked = (int(group_count[0])+1)

            # Determines if the habit inputted by the user is a Weekly or Daily habit
            c.execute("""SELECT periodicity
                FROM habits_table
                WHERE habitName =?""", (habit_name,))
            day_week = c.fetchone()
            day_week1 = 'weeks' if (str(day_week[0]) == 'Weekly') else 'days'

            # Finds the start date of the longest streak for the habit inputted by the user
            c.execute("""SELECT dateCreated
                FROM grouped1
                WHERE habitName =?""", (habit_name,))
            start_date = c.fetchone()
            start_date1 = (datetime.datetime.strptime(start_date[0], '%Y-%m-%d').date() - datetime.timedelta(days=1))
            end_date = (start_date1 + (days_checked * datetime.timedelta(days=1)) - datetime.timedelta(days=1))

            # Tracking weekly performance
            # Creates view "group_ranked" from "performance_table"
            c.execute("""CREATE VIEW group_ranked AS
                SELECT *,
                (week_of_the_year - ranking) AS grouping
                FROM ranked""")

            # Creates view "group_ranked" from view "group_ranked1"
            c.execute("""CREATE VIEW group_ranked1 AS
                SELECT *, COUNT() AS groupCount
                FROM group_ranked
                GROUP BY grouping
                ORDER BY groupCount DESC""")

            # Finds the number of weeks for the longest streak
            c.execute("""SELECT groupCount
                FROM group_ranked1
                WHERE habitName =?""", (habit_name,))
            group_count = c.fetchone()
            weeks_checked = (int(group_count[0]) + 1)

            # Finds the longest streak
            c.execute("""SELECT grouping
                FROM group_ranked1
                WHERE habitName =?""", (habit_name,))
            grouping1 = c.fetchone()
            grouping2 = (int(grouping1[0]))

            # Creates view "group_ranked2" from view "group_ranked"
            c.execute("""CREATE VIEW group_ranked2 AS
                SELECT *
                FROM group_ranked
                ORDER BY dateCreated DESC""")

            # Finds the end week of the streak
            c.execute("""SELECT dateCreated
                FROM group_ranked2
                WHERE grouping =?""", (grouping2,))
            grouping3 = c.fetchone()
            end_date_week = (str(grouping3[0]))

            # Finds the start week of the streak
            c.execute("""SELECT dateCreated
                FROM group_ranked1
                WHERE grouping =?""", (grouping2,))
            grouping5 = c.fetchone()
            start_date_week = (str(grouping5[0]))

            # Output based on whether habit inputted is a weekly or daily habit
            if (str(day_week[0]) == 'Weekly'):
                print(f"\nYour longest streak for {habit_name} is {weeks_checked} {day_week1} starting from {start_date_week} to {end_date_week}")
            else:
                print(f"\nYour longest streak for {habit_name} is {days_checked} {day_week1} starting from {start_date1} to {end_date}")

            # Drop all views that were created
            c.execute("DROP VIEW ranked")
            c.execute("DROP VIEW grouped")
            c.execute("DROP VIEW grouped1")
            c.execute("DROP VIEW group_ranked")
            c.execute("DROP VIEW group_ranked1")
            c.execute("DROP VIEW group_ranked2")

            # The user clicks the run button to carry out another action
            print("Click Rerun to continue")

        else:
            # If the user hasn't selected an existing habit they are instructed to do so
            print('You can only checkoff existing habits. Please select one!')

            # The user clicks the run button to carry out another action
            print("Click Rerun to continue")

    # Executed if option 'D' is entered
    elif (chosen_option == 'D'):

        # Finds the longest streak for weekly habits
        # Creates view "week_ranked" from table "performance_table"
        c.execute("""CREATE VIEW week_ranked AS
            SELECT *,
            ROW_NUMBER() OVER (PARTITION BY habitname ORDER BY dateCreated) AS ranking
            FROM performance_table
            WHERE streak_maintained =='Yes' AND periodicity == 'Weekly'""")

        # Creates view "group_ranked" from view "week_ranked"
        c.execute("""CREATE VIEW group_ranked AS
            SELECT *,
            (week_of_the_year - ranking) AS grouping
            FROM week_ranked""")

        # Creates view "group_ranked1" from view "group_ranked"
        c.execute("""CREATE VIEW group_ranked1 AS
            SELECT *, COUNT() AS groupCount
            FROM group_ranked
            GROUP BY habitName, grouping
            ORDER BY groupCount DESC""")

        # Finds the longest weekly habit
        c.execute("""SELECT groupcount
            FROM group_ranked1""")
        group_count = c.fetchone()
        weeks_checked = (int(group_count[0]) + 1)

        # Finds the habit name of the weekly habit with the longest streak
        c.execute("""SELECT habitName
            FROM group_ranked1""")
        habit_name1 = c.fetchone()
        habit_name2 = (str(habit_name1[0]))

        # Finds the grouping of the weekly habit with the longest streak
        c.execute("""SELECT grouping
            FROM group_ranked1""")
        grouping1 = c.fetchone()
        grouping2 = (int(grouping1[0]))

        # Creates view "week_ranked1" from table "performance_table"
        c.execute("""CREATE VIEW week_ranked1 AS
            SELECT *,
            ROW_NUMBER() OVER (PARTITION BY habitname ORDER BY dateCreated) AS ranking
            FROM performance_table
            WHERE periodicity == 'Weekly'""")

        # Creates view "group_ranked2" from view "week_ranked1"
        c.execute("""CREATE VIEW group_ranked2 AS
            SELECT *,
            (week_of_the_year - ranking) AS grouping
            FROM week_ranked1
            ORDER BY dateCreated""")

        # Calculates the start week
        start_date_grouping = grouping2 - 1
        c.execute("""SELECT dateCreated
            FROM group_ranked2
            WHERE grouping =?""", (start_date_grouping,))
        grouping3 = c.fetchone()
        start_date_week1 = (str(grouping3[0]))

        # Creates view "group_ranked3" from view "group_ranked"
        c.execute("""CREATE VIEW group_ranked3 AS
            SELECT *
            FROM group_ranked
            ORDER BY dateCreated DESC""")

        # Calculates the end week
        c.execute("""SELECT dateCreated
            FROM group_ranked3
            WHERE grouping =?""", (grouping2,))
        grouping5 = c.fetchone()
        end_date_week1 = (str(grouping5[0]))

        # Drops all views that were created
        c.execute("DROP VIEW week_ranked")
        c.execute("DROP VIEW week_ranked1")
        c.execute("DROP VIEW group_ranked")
        c.execute("DROP VIEW group_ranked1")
        c.execute("DROP VIEW group_ranked2")
        c.execute("DROP VIEW group_ranked3")

        # Finds the longest streak for daily habits
        # Creates view "ranked" from table "performance_table"
        c.execute("""CREATE VIEW ranked AS
            SELECT *,
            ROW_NUMBER() OVER (PARTITION BY habitname ORDER BY dateCreated) AS ranking,
            julianday(dateCreated) AS julian
            FROM performance_table
            WHERE periodicity == 'Daily'""")

        # Creates view "grouped" from view "ranked"
        c.execute("""CREATE VIEW grouped AS
            SELECT *,
            (julian - ranking) AS grouping
            FROM ranked""")

        # Creates view "grouped1" from view "grouped"
        c.execute("""CREATE VIEW grouped1 AS
            SELECT *, COUNT() AS groupCount
            FROM grouped
            WHERE streak_maintained =='Yes'
            GROUP BY habitName, grouping
            ORDER BY groupCount DESC""")

        # Calculate the longest streak for daily habits
        c.execute("""SELECT groupcount
            FROM grouped1""")
        group_count = c.fetchone()
        days_checked = (int(group_count[0]) + 1)

        # Finds the name of the daily habit with the longest streak
        c.execute("""SELECT habitName
                   FROM grouped1""")
        habit_name3 = c.fetchone()
        habit_name4 = (str(habit_name3[0]))

        # Calculates the start date of the daily habit with the longest streak
        c.execute("""SELECT dateCreated
            FROM grouped1""")
        start_date1 = c.fetchone()
        start_date2 = (datetime.datetime.strptime(start_date1[0], '%Y-%m-%d').date() - datetime.timedelta(days=1))

        # Calculates the end date of the daily habit with the longest streak
        end_date1 = (start_date2 + (days_checked * datetime.timedelta(days=1)) - datetime.timedelta(days=1))

        # Drops all views that were created
        c.execute("DROP VIEW ranked")
        c.execute("DROP VIEW grouped")
        c.execute("DROP VIEW grouped1")

        # compares the streaks of the longest weekly habit with that of the daily habit and outputs the longer of the two
        # where there is a tie, both streaks are outputted
        if (weeks_checked > days_checked):
            print(f"\nYour longest streak is {habit_name2} for {weeks_checked} weeks starting from {start_date_week1} to {end_date_week1}.")
        elif (weeks_checked < days_checked):
            print(f"\nYour longest streak is {habit_name4} for {days_checked} days starting from {start_date2} to {end_date1}.")
        else:
            print('We have a tie for weekly and daily habits!')
            print(f"\nYour longest streak is {habit_name2} for {days_checked} weeks starting from {start_date2} to {end_date1}.")
            print(f"\nYour longest streak is {habit_name4} for {days_checked} days starting from {start_date2} to {end_date1}.")

        # The user clicks the run button to carry out another action
        print("Click Rerun to continue")

    else:
        # if the user hasn't chosen from option A, B, C and D, they are asked to choose a one of these options
        print('Please choose from options A, B, C or D')

        # The user clicks the run button to carry out another action
        print("Click Rerun to continue")







