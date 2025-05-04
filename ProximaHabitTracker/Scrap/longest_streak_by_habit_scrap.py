import datetime
# # SQLite3 used to create a database
import sqlite3
import pandas as pd
from tabulate import tabulate


# Used to create the connection to the database
conn = sqlite3.connect('../habits_database.db')
# Used to create cursor object
c = conn.cursor()

# Used to prompt the user to provide the name of the habit
habit_name = input('\nEnter the name of the habit you would like to see the longest run streak for: ')

# Tracking daily performance
# Creates view "ranked" from table "performance_table"
c.execute("""CREATE VIEW ranked AS
    SELECT habitName, dateCreated, week_of_the_year, streak_maintained, periodicity,
    ROW_NUMBER() OVER (PARTITION BY streak_maintained ORDER BY habitName) AS ranking,
    julianday(dateCreated) AS julian
    FROM performance_table   
    WHERE streak_maintained == 'Yes'""")

my_data = [c]

# Used to create a view of all habits
c.execute("SELECT * FROM ranked")

# Used to create a table of the data selected
for x in my_data:
    df = pd.DataFrame(x)
    print(tabulate(df, headers=["No.", "Habit Name", "Date Created", "Week of the Year", "StreakMaintained", "Periodicity", "Ranking", "Julian"], tablefmt='psql'))

# Creates view "grouped" from view "ranked"
c.execute("""CREATE VIEW grouped AS
    SELECT *,
        (ranking - julian) AS grouping
    FROM ranked""")


c.execute("SELECT * FROM grouped")

# Used to create a table of the data selected
for x in my_data:
    df = pd.DataFrame(x)
    print(tabulate(df, headers=["No.", "Habit Name", "Date Created", "Week of the Year", "StreakMaintained", "Periodicity", "Ranking", "Julian", "Grouping"], tablefmt='psql'))

# Creates view "grouped1" from view "grouped"
c.execute("""CREATE VIEW grouped1 AS
    SELECT *, COUNT() AS groupCount
    FROM grouped
    GROUP BY grouping
    ORDER BY groupCount DESC""")


c.execute("SELECT * FROM grouped1")

# Used to create a table of the data selected
for x in my_data:
    df = pd.DataFrame(x)
    print(tabulate(df, headers=["No.", "Habit Name", "Date Created", "Week of the Year", "StreakMaintained", "Periodicity", "Ranking", "Julian", "Grouping", "Group Count"], tablefmt='psql'))

# Finds the longest streak for the habit selected
c.execute("""SELECT groupCount
    FROM grouped1
    WHERE habitName =?""", (habit_name,))
group_count = c.fetchone()
days_checked = (int(group_count[0]) + 1)
print(days_checked)


# Tracking weekly performance
# Creates view "group_ranked" from view "week_ranked"
c.execute("""CREATE VIEW group_ranked AS
    SELECT *,
    (week_of_the_year - ranking) AS grouping
    FROM ranked""")

c.execute("SELECT * FROM group_ranked")

# Used to create a table of the data selected
for x in my_data:
    df = pd.DataFrame(x)
    print(tabulate(df, headers=["No.", "Habit Name", "Date Created", "Week of the Year", "StreakMaintained", "Periodicity", "Ranking",  "Julian", "Grouping"], tablefmt='psql'))

# Creates view "group_ranked" from view "group_ranked1"
c.execute("""CREATE VIEW group_ranked1 AS
    SELECT *, COUNT() AS groupCount
    FROM group_ranked
    GROUP BY grouping
    ORDER BY groupCount DESC""")

c.execute("SELECT * FROM group_ranked1")

# Used to create a table of the data selected
for x in my_data:
    df = pd.DataFrame(x)
    print(tabulate(df, headers=["No.", "Habit Name", "Date Created", "Week of the Year", "StreakMaintained", "Periodicity", "Ranking",  "Julian", "Grouping", "Group Count"], tablefmt='psql'))

# Finds the longest streak for the habit selected
c.execute("""SELECT groupCount
    FROM group_ranked1
    WHERE habitName =?""", (habit_name,))
group_count = c.fetchone()
weeks_checked = (int(group_count[0]) + 1)
print(weeks_checked)

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

c.execute("SELECT * FROM group_ranked2")

# Used to create a table of the data selected
for x in my_data:
    df = pd.DataFrame(x)
    print(tabulate(df, headers=["No.", "Habit Name", "Date Created", "Week of the Year", "StreakMaintained", "Periodicity", "Ranking",  "Julian", "Grouping", "Group Count"], tablefmt='psql'))

# Finds the end week of the streak
c.execute("""SELECT dateCreated
    FROM group_ranked2
    WHERE grouping =?""", (grouping2,))
grouping3 = c.fetchone()
end_date_week = (str(grouping3[0]))
print(end_date_week)

# Finds the start week of the streak
c.execute("""SELECT dateCreated
    FROM group_ranked1
    WHERE grouping =?""", (grouping2,))
grouping5 = c.fetchone()
start_date_week = (str(grouping5[0]))
print(start_date_week)

# # Output based on whether habit inputted is a weekly or daily habit
# if (str(day_week[0]) == 'Weekly'):
#     print(f"\nYour longest streak for {habit_name} is {weeks_checked} {day_week1} starting from {start_date_week} to {end_date_week}")
# else:
#     print(f"\nYour longest streak for {habit_name} is {days_checked} {day_week1} starting from {start_date1} to {end_date}")

# Drop all views that were created
c.execute("DROP VIEW ranked")
c.execute("DROP VIEW grouped")
c.execute("DROP VIEW grouped1")
c.execute("DROP VIEW group_ranked")
c.execute("DROP VIEW group_ranked1")
c.execute("DROP VIEW group_ranked2")