from flask import Flask, request
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime


app = Flask(__name__)


@app.route('/getlasthour', methods=['GET'])
def get_last_hour():
    try:
        conn = psycopg2.connect("dbname='mtalostfound' user='mtasubway' host='web432.webfaction.com' password='123456'")
    except:
        print "I am unable to connect to the database"

    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("""select category, subcategory, count, max(importtime) from items
                group by category, subcategory, count
                order by category,subcategory;""")

    json_output = json.dumps(cur.fetchall(), default=json_serial)

    return json_output

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial

@app.route('/gettotals', methods=['GET'])
def get_totals():
    try:
        conn = psycopg2.connect("dbname='mtalostfound' user='mtasubway' host='web432.webfaction.com' password='123456'")
    except:
        print "I am unable to connect to the database"

    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("""select lostcount, claimcount, max(importtime) from totals
                group by lostcount, claimcount;""")

    json_output = json.dumps(cur.fetchall(), default=json_serial)

    return json_output

if __name__ == '__main__':
    app.run()
