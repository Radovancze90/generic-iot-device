import sched, time
import mysql.connector as mysql
import paho.mqtt.publish as publish

s = sched.scheduler(time.time, time.sleep)
mysql_connection = None
query_fetch_device_action = ("SELECT da.id, da.action, d.mac "
    "FROM main_deviceaction da "
    "INNER JOIN main_device d ON d.id = da.device_id "
    "WHERE da.created_at <= NOW() AND da.finished_at IS NULL "
    "ORDER BY da.created_at ASC "
    "LIMIT 1")
query_finish_device_action = ("UPDATE main_deviceaction SET finished_at = NOW() WHERE id = %s")

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

def execute_device_action(id, action, mac):
    global mysql_connection

    print("{}, {}, {}".format(id, action, mac)) # TODO: rm debug

    if action.lower() in ("relay_on", "relay_off"):
        cursor = get_mysql_cursor()

        cursor.execute(query_finish_device_action, (id,))
        cursor.close()
        mysql_connection.commit()

        publish.single(("bullstone/v1/" + mac + "/relay/0/set"),
            payload = ("1" if action.lower() == "relay_on" else "0"),
            qos = 2,
            hostname = "192.168.0.100", # sem dej nějakou doménu ke ke které se budou připojovat zařízení přes MQTT
            port = 1883,
            auth = {"username":"mqtt_bridge", "password":"QDEswXqn39SoC5i4"})

def fetch_device_action(sc):
    global mysql_connection

    cursor = get_mysql_cursor()
    cursor.execute(query_fetch_device_action,)

    action = cursor.fetchone()

    cursor.close()
    mysql_connection.commit()

    if action is not None:
        execute_device_action(action[0], action[1], action[2])

    s.enter(1, 1, fetch_device_action, (sc,))

init_mysql_connection()

s.enter(1, 1, fetch_device_action, (s,))
s.run()
