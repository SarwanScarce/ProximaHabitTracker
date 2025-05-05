import pytest
# Used to import datetime class
import datetime
# SQLite3 used to create a database
import sqlite3


# Used to test the function to calculate the longest run streak for the 1st preloaded habit, Running
def test_longest_run_streak_running():
    # Used to create the connection to the database
    conn = sqlite3.connect('habits_database.db')
    # Used to create cursor object
    c = conn.cursor()

    # Used to prompt the user to provide the name of the habit
    habit_name = 'Running'

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
        days_checked = (int(group_count[0]) + 1)

        # Finds the start date of the longest streak for the habit inputted by the user
        c.execute("""SELECT dateCreated
                    FROM grouped1
                    WHERE habitName =?""", (habit_name,))
        start_date = c.fetchone()
        start_date1 = (datetime.datetime.strptime(start_date[0], '%Y-%m-%d').date() - datetime.timedelta(days=1))
        end_date = (start_date1 + (days_checked * datetime.timedelta(days=1)) - datetime.timedelta(days=1))

        # Drop all views that were created
        c.execute("DROP VIEW ranked")
        c.execute("DROP VIEW grouped")
        c.execute("DROP VIEW grouped1")

        result = days_checked
        result1 = start_date1
        result2 = end_date

    assert result == 6
    assert result1 == datetime.datetime.strptime('2025-04-12', '%Y-%m-%d').date()
    assert result2 == datetime.datetime.strptime('2025-04-17', '%Y-%m-%d').date()


# Used to test the function to calculate the longest run streak for the 2nd preloaded habit, Swimming
def test_longest_run_streak_swimming():
    # Used to create the connection to the database
    conn = sqlite3.connect('habits_database.db')
    # Used to create cursor object
    c = conn.cursor()

    # Used to prompt the user to provide the name of the habit
    habit_name = 'Swimming'

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
        days_checked = (int(group_count[0]) + 1)

        # Finds the start date of the longest streak for the habit inputted by the user
        c.execute("""SELECT dateCreated
                    FROM grouped1
                    WHERE habitName =?""", (habit_name,))
        start_date = c.fetchone()
        start_date1 = (datetime.datetime.strptime(start_date[0], '%Y-%m-%d').date() - datetime.timedelta(days=1))
        end_date = (start_date1 + (days_checked * datetime.timedelta(days=1)) - datetime.timedelta(days=1))

        # Drop all views that were created
        c.execute("DROP VIEW ranked")
        c.execute("DROP VIEW grouped")
        c.execute("DROP VIEW grouped1")

        result = days_checked
        result1 = start_date1
        result2 = end_date

    assert result == 4
    assert result1 == datetime.datetime.strptime('2025-04-06', '%Y-%m-%d').date()
    assert result2 == datetime.datetime.strptime('2025-04-09', '%Y-%m-%d').date()


# Used to test the function to calculate the longest run streak for the 5th preloaded habit, Reading
def test_longest_run_streak_reading():
    # Used to create the connection to the database
    conn = sqlite3.connect('habits_database.db')
    # Used to create cursor object
    c = conn.cursor()

    # Used to prompt the user to provide the name of the habit
    habit_name = 'Reading'

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
        days_checked = (int(group_count[0]) + 1)

        # Finds the start date of the longest streak for the habit inputted by the user
        c.execute("""SELECT dateCreated
                    FROM grouped1
                    WHERE habitName =?""", (habit_name,))
        start_date = c.fetchone()
        start_date1 = (datetime.datetime.strptime(start_date[0], '%Y-%m-%d').date() - datetime.timedelta(days=1))
        end_date = (start_date1 + (days_checked * datetime.timedelta(days=1)) - datetime.timedelta(days=1))

        # Drop all views that were created
        c.execute("DROP VIEW ranked")
        c.execute("DROP VIEW grouped")
        c.execute("DROP VIEW grouped1")

        result = days_checked
        result1 = start_date1
        result2 = end_date

    assert result == 5
    assert result1 == datetime.datetime.strptime('2025-04-23', '%Y-%m-%d').date()
    assert result2 == datetime.datetime.strptime('2025-04-27', '%Y-%m-%d').date()


# Used to test the function to calculate the longest run streak for the 3rd preloaded habit, Hiking
def test_longest_run_streak_hiking():
    # Used to create the connection to the database
    conn = sqlite3.connect('habits_database.db')
    # Used to create cursor object
    c = conn.cursor()

    # Used to prompt the user to provide the name of the habit
    habit_name = 'Hiking'

    # Used to create a table of the data selected based on the habit name inputted
    sql = "SELECT * FROM habits_table WHERE habitName ='{}'".format(habit_name)
    c.execute(sql)

    # Executes if a valid habit is found
    if c.fetchall():

        # Tracking weekly performance
        # Creates view "ranked" from table "performance_table"
        c.execute("""CREATE VIEW ranked AS
            SELECT habitName, dateCreated, week_of_the_year, streak_maintained, periodicity,
            ROW_NUMBER() OVER (PARTITION BY streak_maintained ORDER BY habitName) AS ranking,
            julianday(dateCreated) AS julian
            FROM performance_table   
            WHERE streak_maintained == 'Yes'""")

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

        c.execute("DROP VIEW ranked")
        c.execute("DROP VIEW group_ranked")
        c.execute("DROP VIEW group_ranked1")
        c.execute("DROP VIEW group_ranked2")

        result = weeks_checked
        result1 = start_date_week
        result2 = end_date_week

    assert result == 6
    assert result1 == '2025-03-24'
    assert result2 == '2025-04-24'


# Used to test the function to calculate the longest run streak for the 4th preloaded habit, Skiing
def test_longest_run_streak_skiing():
    # Used to create the connection to the database
    conn = sqlite3.connect('habits_database.db')
    # Used to create cursor object
    c = conn.cursor()

    # Used to prompt the user to provide the name of the habit
    habit_name = 'Skiing'

    # Used to create a table of the data selected based on the habit name inputted
    sql = "SELECT * FROM habits_table WHERE habitName ='{}'".format(habit_name)
    c.execute(sql)

    # Executes if a valid habit is found
    if c.fetchall():

        # Tracking weekly performance
        # Creates view "ranked" from table "performance_table"
        c.execute("""CREATE VIEW ranked AS
            SELECT habitName, dateCreated, week_of_the_year, streak_maintained, periodicity,
            ROW_NUMBER() OVER (PARTITION BY streak_maintained ORDER BY habitName) AS ranking,
            julianday(dateCreated) AS julian
            FROM performance_table   
            WHERE streak_maintained == 'Yes'""")

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

        c.execute("DROP VIEW ranked")
        c.execute("DROP VIEW group_ranked")
        c.execute("DROP VIEW group_ranked1")
        c.execute("DROP VIEW group_ranked2")

        result = weeks_checked
        result1 = start_date_week
        result2 = end_date_week

    assert result == 4
    assert result1 == '2025-04-10'
    assert result2 == '2025-04-26'


# Used to test the function to calculate the longest run streak
def test_longest_run_streak():
    # Finds the longest streak for weekly habits
    # Used to create the connection to the database
    conn = sqlite3.connect('habits_database.db')
    # Used to create cursor object
    c = conn.cursor()

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
        print(
            f"\nYour longest streak is {habit_name2} for {weeks_checked} weeks starting from {start_date_week1} to {end_date_week1}.")
    elif (weeks_checked < days_checked):
        print(
            f"\nYour longest streak is {habit_name4} for {days_checked} days starting from {start_date2} to {end_date1}.")
    else:
        print('We have a tie for weekly and daily habits!')
        print(
            f"\nYour longest streak is {habit_name2} for {days_checked} weeks starting from {start_date_week1} to {end_date_week1}.")
        print(
            f"\nYour longest streak is {habit_name4} for {days_checked} days starting from {start_date2} to {end_date1}.")


        result = weeks_checked
        result1 = start_date_week1
        result2 = end_date_week1
        result3 = days_checked
        result4 = start_date2
        result5 = end_date1

    assert result == 6
    assert result1 == '2025-03-20'
    assert result2 == '2025-04-24'
    assert result3 == 6
    assert result4 == datetime.datetime.strptime('2025-04-12', '%Y-%m-%d').date()
    assert result5 == datetime.datetime.strptime('2025-04-17', '%Y-%m-%d').date()