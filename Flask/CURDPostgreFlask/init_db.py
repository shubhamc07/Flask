import psycopg2

conn =psycopg2.connect(database="flask_db",host="localhost",user="postgres",password="shubham",port="5432")
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS courses(id serial PRIMARY KEY,name varchar(100),fees integer,duration integer);''')
cur.execute('''INSERT INTO courses(name,fees,duration)VALUES('python',6500,45),('java',6000,30),('javascript',7000,40)''')


conn.commit()
cur.close()
conn.close()