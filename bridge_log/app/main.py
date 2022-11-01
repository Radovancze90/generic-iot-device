import re
import mysql.connector as mysql
import paho.mqtt.client as mqtt

mysql_connection = None
query_persist_device = ("INSERT INTO main_device (mac, created_at) VALUES (%s, NOW())")
query_persist_device_log = ("INSERT INTO main_devicelog (device_id, option, value, created_at) VALUES ((SELECT id FROM main_device WHERE mac = %s LIMIT 1), %s, %s, NOW())")
query_persist_device_log_update = ("UPDATE main_devicelog SET value=%s, created_at=NOW() WHERE option=%s AND device_id=(SELECT id FROM main_device WHERE mac = %s LIMIT 1) LIMIT 1")
query_persist_device_log_exists = ("SELECT * FROM main_devicelog WHERE option=%s AND device_id=(SELECT id FROM main_device WHERE mac = %s LIMIT 1) LIMIT 1")
query_persist_device_exists = ("SELECT * FROM main_device WHERE device_id=(SELECT id FROM main_device WHERE mac = %s LIMIT 1) LIMIT 1")

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

def create_device(mac):
    global mysql_connection

    try:
        cursor=get_mysql_cursor()
        
        data=cursor.execute(mac, 'SELECT * FROM main_device WHERE device_id=(SELECT id FROM main_device WHERE mac = %s LIMIT 1) LIMIT 1')
        if len(data)==0:
           cursor.execute(query_persist_device, (mac, ))
           
        cursor.close()
        mysql_connection.commit()

    except Exception:
        pass

def persist_device_log(mac, option, value):
    global mysql_connection

    try:
        if option.lower() in ("app", "version", "board", "host", "ip", "mac", "freeheap", "loadavg", "vcc", "button", "ssid", "rssi", "uptime", "power", "reactive", "factor", "energy"):
          return
            
        exist=query_persist_device_log_exists(option, mac)
        if len(exist)==0:
           cursor = get_mysql_cursor()
           cursor.execute(query_persist_device_log, (mac, option, value))
           cursor.close()
           mysql_connection.commit()
        
    except Exception:
        create_device(mac)

def persist_device_log_update(mac, option, value):
    global mysql_connection

    try:
        if option.lower() in ("app", "version", "board", "host", "ip", "mac", "freeheap", "loadavg", "vcc", "button", "ssid", "rssi", "uptime", "power", "reactive", "factor", "energy"):
          return
        
        cursor = get_mysql_cursor()
        
        cursor.execute(query_persist_device_log_update, (value, option, mac))
        cursor.close()
        mysql_connection.commit()

    except Exception:
        #persist_device_log(mac, option, value)
        create_device(mac)

def on_message(mqttc, obj, msg):
    topicMatchOutput = re.search("^bullstone/v1/([0-9A-Z]+)/([a-z]+)(/0)?/get$", msg.topic) #na začátek jsem dal třeba bullstone to co tam bude na začátku musí být i ve FW v hardware

    if topicMatchOutput is not None:
        mac=topicMatchOutput.group(1)
        option=topicMatchOutput.group(2)
        msgs=msg.payload
        
        try:
           exist=query_persist_device_log_exists(option, mac)
           if len(exist)!=0:
               if option.lower() in ("app", "version", "board", "host", "ip", "mac", "freeheap", "loadavg", "vcc", "button", "ssid", "rssi", "uptime", "power", "reactive", "factor", "energy"):
                    return
               query_persist_device_log_update(msgs, option, mac)
        except Exception:
             persist_device_log(mac, option, msgs)


init_mysql_connection()
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.username_pw_set("mqtt_bridge", "QDEswXqn39SoC5i4")
mqtt_client.connect("192.168.0.100", 1883, 15) # sem dej nějakou doménu ke ke které se budou připojovat zařízení přes MQTT
mqtt_client.subscribe("bullstone/v1/#", 2)
mqtt_client.loop_forever()
