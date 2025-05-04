# Used to import datetime class
import datetime
# SQLite3 used to create a database
import sqlite3


# Used to create the check_streak() function
def check_streak(habit_name):

    # Used to create the connection to the database
    conn = sqlite3.connect('habits_database.db')
    # Used to create cursor object
    c = conn.cursor()


    # Used to call today's date
    today = datetime.date.today()

    # Used to determine last week
    last_week = (today - datetime.timedelta(weeks=1))

    # Used to determine yesterday
    yesterday = today - datetime.timedelta(days=1)

    # Used to create a table from the habits_table using the habit name inputted to determine whether a habit is daly or weekly
    c.execute("SELECT periodicity FROM habits_table WHERE habitName=?", (habit_name,))
    weekly_daily = c.fetchone()
    weekly_daily_str = "".join(weekly_daily[0])
    if weekly_daily_str == 'Weekly':

        # Used to create the performance_records view of all records sorted in descending order.
        c.execute("CREATE VIEW performance_records AS SELECT * FROM performance_table ORDER BY dateCreated DESC")

        # Used to find the last checkoff date using the habit name inputted
        c.execute("SELECT dateCreated FROM performance_records WHERE habitName=?", (habit_name,))
        last_checkoff = c.fetchone()

        # Used to drop the performance_records view
        c.execute("DROP VIEW performance_records")

        # Determines if the streak was maintained based on the last check off date
        if c.fetchall():
            last_checkoff_converted = datetime.datetime.strptime(last_checkoff[0], '%Y-%m-%d').date()
            if last_checkoff_converted.strftime("%V") == last_week.strftime("%V"):
                return ('Yes')
            else:
                return ('No')
        else:
            return ('No')
    else:
        # Used to create a view of all records sorted in descending order.
        c.execute("CREATE VIEW performance_records AS SELECT * FROM performance_table ORDER BY dateCreated DESC")

        # Used to find the last checkoff date using the habit name inputted
        c.execute("SELECT dateCreated FROM performance_records WHERE habitName=?", (habit_name,))
        last_checkoff = c.fetchone()

        # Used to drop the performance_records view
        c.execute("DROP VIEW performance_records")

        # Determines if the streak was maintained based on the last check off date
        if c.fetchall():
            last_checkoff_converted = datetime.datetime.strptime(last_checkoff[0], '%Y-%m-%d').date()
            if last_checkoff_converted == yesterday:
                return ("Yes")
            else:
                return ('No')
        else:
            return ('No')