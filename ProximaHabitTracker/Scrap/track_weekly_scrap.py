# import datetime
# # SQLite3 used to create a database
import sqlite3
import pandas as pd
from tabulate import tabulate


# Used to create the connection to the database
conn = sqlite3.connect('habits_database.db')
c = conn.cursor()

# Used to prompt the user to provide the name of the habit

c.execute("""CREATE VIEW week_ranked AS
    SELECT *,
    ROW_NUMBER() OVER (PARTITION BY streak_maintained ORDER BY dateCreated) AS ranking
    FROM performance_table
    WHERE streak_maintained =='Yes' AND periodicity == 'Weekly'""")

c.execute("SELECT * FROM week_ranked")

my_data = [c]

for x in my_data:
    df = pd.DataFrame(x)
    print(tabulate(df, headers='keys', tablefmt='psql'))


c.execute("""CREATE VIEW group_ranked AS
    SELECT *,
    (week_of_the_year - ranking) AS grouping
    FROM week_ranked""")

c.execute("SELECT * FROM group_ranked")

my_data = [c]

for x in my_data:
    df = pd.DataFrame(x)
    print(tabulate(df, headers='keys', tablefmt='psql'))


c.execute("""CREATE VIEW group_ranked1 AS
    SELECT *, COUNT() AS groupCount
    FROM group_ranked
    GROUP BY grouping
    ORDER BY groupCount DESC""")

c.execute("SELECT * FROM group_ranked1")

my_data = [c]

for x in my_data:
    df = pd.DataFrame(x)
    print(tabulate(df, headers='keys', tablefmt='psql'))


c.execute("""SELECT groupcount
    FROM group_ranked1""")
group_count = c.fetchone()
weeks_checked = (int(group_count[0]) + 1)
print(weeks_checked)


c.execute("""SELECT grouping
    FROM group_ranked1""")
grouping1 = c.fetchone()
grouping2 = (int(grouping1[0]))
print(grouping2)


c.execute("""CREATE VIEW group_ranked2 AS
    SELECT *
    FROM group_ranked
    ORDER BY dateCreated DESC""")

c.execute("SELECT * FROM group_ranked2")

my_data = [c]

for x in my_data:
    df = pd.DataFrame(x)
    print(tabulate(df, headers='keys', tablefmt='psql'))


c.execute("""SELECT dateCreated
    FROM group_ranked2
    WHERE grouping =?""", (grouping2,))
grouping3 = c.fetchone()
grouping4 = (str(grouping3[0]))
print(grouping4)


c.execute("""SELECT dateCreated
    FROM group_ranked1
    WHERE grouping =?""", (grouping2,))
grouping5 = c.fetchone()
grouping6 = (str(grouping5[0]))
print(grouping6)


c.execute("DROP VIEW week_ranked")
c.execute("DROP VIEW group_ranked")
c.execute("DROP VIEW group_ranked1")
c.execute("DROP VIEW group_ranked2")


conn.commit()
print("Click Rerun to continue")
c.close()





