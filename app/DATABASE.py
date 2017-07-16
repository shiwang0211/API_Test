import sqlite3
conn=sqlite3.connect('test2.db')
c=conn.cursor()
sql_lines= open('test.sql','r').read()
c.executescript(sql_lines)
c.executescript('select * from entries') #for testing purpose
c.close()


