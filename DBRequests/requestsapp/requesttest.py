import psycopg2

try:
    conn = psycopg2.connect("dbname='mtalostfound' user='mtasubway' host='web432.webfaction.com' password='123456'")
except:
    print "I am unable to connect to the database"

cur = conn.cursor()

cur.execute("""SELECT * from items""")

rows = cur.fetchall()
for row in rows:
    print row
