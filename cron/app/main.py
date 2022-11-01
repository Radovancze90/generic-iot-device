import datetime
import mysql.connector as mysql

d = datetime.datetime.now()
day_of_week = d.weekday() + 1
day_of_month = d.day
hour = d.hour
minute = d.minute

mysql_connection = None
query_fetch_device_cron = ("SELECT dc.device_id, dc.action "
    "FROM main_devicecron dc "
    "WHERE dc.created_at <= NOW() AND (dc.day_of_week = 0 OR dc.day_of_week = %s)  AND (dc.day_of_month = 0 OR dc.day_of_month = %s) AND dc.hour = %s AND dc.minute = %s "
    "ORDER BY dc.id ASC ")
query_persist_device_action = ("INSERT INTO main_deviceaction (device_id, action, created_at) VALUES (%s, %s, NOW())")

def init_mysql_connection():
    global mysql_connection

    mysql_connection = mysql.connect(host="db", user="root", password="DB PASS", database="web")

def get_mysql_cursor():
    global mysql_connection

    try:
        mysql_connection.ping(reconnect=True, attempts=3, delay=5)
    except mysql.connector.Error as err:
        init_mysql_connection()

    return mysql_connection.cursor()

init_mysql_connection()

cursor = get_mysql_cursor()
cursor.execute(query_fetch_device_cron, (day_of_week, day_of_month, hour, minute))

rows = []

for row in cursor:
    rows.append(row)

for row in rows:
    cursor.execute(query_persist_device_action, row)

mysql_connection.commit()
