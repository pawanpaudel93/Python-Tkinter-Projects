import psycopg2

conn = psycopg2.connect("host='localhost' dbname='dbmsprojectt' user='postgres' password='admin'")
curs = conn.cursor()
curs.execute(open('student_schema.sql', 'r').read())
