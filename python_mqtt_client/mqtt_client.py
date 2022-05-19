import paho.mqtt.client as mqtt
import sqlite3
from datetime import datetime

pump_start_time ={ 'tomato' : "", 'chilli' : "", 'sample' : ""}
pump_stop_time ={ 'tomato' : "", 'chilli' : "", 'sample' : ""}
path_to_db = ""

def insert_sensor_data_into_db(mlevel, table_name, timestamp):
    sql_conn = sqlite3.connect(path_to_db)
    sql_cursor = sql_conn.cursor()
    sql_cursor.execute("INSERT OR REPLACE INTO "+table_name+" VALUES (:date_time, :mlevel)", {'date_time': timestamp, 'mlevel':mlevel})
    sql_conn.commit()
    sql_conn.close()

def insert_pump_data_into_db(table_name, start_time, stop_time):
    sql_conn = sqlite3.connect(path_to_db)
    sql_cursor = sql_conn.cursor()
    sql_cursor.execute("INSERT OR REPLACE INTO "+table_name+" VALUES (:start_time, :stop_time)", {'start_time': start_time, 'stop_time':stop_time})
    sql_conn.commit()
    sql_conn.close()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("esp8266/tomato")
    client.subscribe("esp8266/chilli")
    client.subscribe("esp8266/sample")    

 
def process_message(msg, table_name):
    if "PUMP_START" in str(msg.payload):
        print(str(datetime.now())+" "+msg.topic+" "+str(msg.payload))
        pump_start_time[table_name] = datetime.now().isoformat()
    elif "PUMP_STOP" in str(msg.payload):
        print(str(datetime.now())+" "+msg.topic+" "+str(msg.payload))
        pump_stop_time[table_name] = datetime.now().isoformat()
        if pump_start_time[table_name] != "" and pump_stop_time[table_name] != "":
            insert_pump_data_into_db(table_name+"_pump", pump_start_time[table_name] , pump_stop_time[table_name] )
        pump_start_time[table_name] = ""
        pump_stop_time[table_name] = ""
    elif "NOOP" in str(msg.payload):
        pass
    else:
        print(str(datetime.now())+" "+msg.topic+" "+str(msg.payload))
        try:
            mlevel = int(msg.payload)
            insert_sensor_data_into_db(mlevel, table_name, datetime.now().isoformat())
        except:
            pass

def on_message(client, userdata, msg):
    
    if msg.topic == "esp8266/tomato":
        process_message(msg, "tomato")
    elif msg.topic == "esp8266/chilli":
        process_message(msg, "chilli")
    elif msg.topic == "esp8266/sample":
        process_message(msg, "sample")


mqtt_broker_username = ""
mqtt_broker_password = ""
mqtt_broker_ip = ""
mqtt_broker_port = 1883
mqtt_brokder_keepalive = 60  

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(mqtt_broker_username, mqtt_broker_password)
client.connect(mqtt_broker_ip, mqtt_broker_port, mqtt_connect_keepalive)


client.loop_forever()
