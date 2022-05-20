

# pip3 install Flask
# pip3 install Flask-RESTful

try:
    from flask import Flask
    from flask_restful import Resource,Api
    from flask_restful import reqparse
    from flask import request
    from datetime import datetime
    import paho.mqtt.client as mqtt
    import json
    import random
    
    import sqlite3
    from sqlite3 import Error

    print("All modules loaded ")
except Exception as e:
    print("Error: {}".format(e))

app = Flask(__name__)
api = Api(app)

pumpChilliValue = 0
pumpTomatoValue = 0
client = None

#------------------------------- DB --------------------------------------------
#
#
#


#------------------------------- DB Connection --------------------------------------------

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn
#------------------------------------------------------------------------------


#------------------------------- DB List Table Name --------------------------------------------

def list_all_tables(conn):
    """
    Query all rtables in the DB
    :param conn: the Connection object
    :return:
    """
    tableName = ['tomato', 'chilli']
    
    '''
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name");

        rows = cur.fetchall()

    for row in rows:
        #print(row[0])
        tableName.append(row[0])
        
        '''

    return tableName
#------------------------------------------------------------------------------


#---------------------------------- Get latest value from DB --------------------------------------------
def select_latestValue(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    currentState = []
    
    cur = conn.cursor()
    
    
    
    #print(plantName)
    
    #print(plantName[0])
    #print(plantName[1])
    
    #cur.execute("SELECT * FROM tomato ORDER BY date_time DESC LIMIT 1")
    query1 = "SELECT * FROM chilli ORDER BY date_time DESC LIMIT 1"
    cur.execute(query1)
    rows = cur.fetchall()
    currentState.append(rows[0])
    #print(rows[0])
    
    query2 = "SELECT * FROM tomato ORDER BY date_time DESC LIMIT 1"
    cur.execute(query2)
    rows = cur.fetchall()
    currentState.append(rows[0])
    #print(rows[0])
    
    #print(currentState)
    
    return currentState
#------------------------------------------------------------------------------


#------------------------------- Query all values from DB --------------------------------------------

def select_all_Values(conn,tableName):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    
    query = "SELECT * FROM " + tableName
    cur.execute(query)
    #cur.execute("SELECT * FROM tomato ORDER BY date_time DESC LIMIT 1000")
    
    rowsAll = cur.fetchall()
    #rowsAll.reverse()
    #print(rowsAll)
    print("--> Total Entries =",len(rowsAll))
    
    jsonString = {}
    hourAndValue = []
    
    # average all moisture value for the hour
    numReadingsPerHour = 0
    hourlySum = 0
    lastHour = -1
    lastDay = -1
    
    for i in range (len(rowsAll)):
       
        currentReading = datetime.strptime(rowsAll[i][0], "%Y-%m-%dT%H:%M:%S.%f")
        #print(currentReading)
       
        currentHour = currentReading.hour
        currentDay = currentReading.day
        
       
        
    
        if(lastHour != currentHour and lastHour != -1):
            
            if numReadingsPerHour > 0:
                value = (int)(hourlySum/numReadingsPerHour)
            else:
                value = 0
            
            # Convert moisture value as 0 to 100
            value = 0 + (100 - 0) * (value - 900) / (300 - 900);
            hourAndValue.append(  (lastHour , (int)(value) ) )
            
            numReadingsPerHour = 0
            hourlySum = 0
            #print("-->HOUR",lastHour)
            
        
        if(lastDay != currentDay and lastDay != -1):
            previousDate = datetime.strptime(rowsAll[i-1][0], "%Y-%m-%dT%H:%M:%S.%f")
            log_date = previousDate.strftime("%m-%d-%y")
            jsonString[log_date] =  hourAndValue
            #print(hourAndValue)
            hourAndValue = []
            #print("------>DAY",lastDay) 
           
        else:
            hourlySum = hourlySum+rowsAll[i][1]
            numReadingsPerHour = numReadingsPerHour+1         
        
            
        lastHour = currentHour
        lastDay = currentDay
                
    # For the incomplete last hour
    if numReadingsPerHour > 0:
        value = (int)(hourlySum/numReadingsPerHour)
    else:
        value = 0
        
    value = 0 + (100 - 0) * (value - 900) / (300 - 900);
    hourAndValue.append(  (lastHour , (int)(value) ) )
    
    previousDate = datetime.strptime(rowsAll[len(rowsAll)-1][0], "%Y-%m-%dT%H:%M:%S.%f")
    log_date = previousDate.strftime("%m-%d-%y")
    jsonString[log_date] = hourAndValue
            
    
    
    if(tableName == 'chilli'):
        return { "pump_chilli" : pumpChilliValue, tableName : jsonString }
    elif(tableName == 'tomato'):
        return { "pump_tomato" : pumpTomatoValue, tableName : jsonString }
    #print(jsonString)
    
    
#------------------------------------------------------------------------------





#----------------------------------Current Moisture Value--------------------------------------------

class currentMoistureValue(object):

    def __init__(self):
        pass

    def get(self):
        
        database = r"sensor_data.db"

        # create a database connection
        conn = create_connection(database)
        print("---DB Connected")

        #plantName = list_all_tables(conn)
        
        latestMoistureValues = select_latestValue(conn)
        
        # Convert moisture value as 0 to 100
        plant1Value = latestMoistureValues[0][1]
        plant1Value = (int)( 0 + (100 - 0) * (plant1Value - 900) / (300 - 900));
        # Convert moisture value as 0 to 100
        plant2Value = latestMoistureValues[1][1]
        plant2Value = (int)( 0 + (100 - 0) * (plant2Value - 900) / (300 - 900));
        
        
        
        
        #print("============> The pump value for dashboard - Also update value here")
        
        '''
        #Pump Value determining
        if(plant1Value < 50 or plant2Value <50):
            pumpValue = 1
        else:
            pumpValue = 0
    '''
        
        conn.close()
        
        if latestMoistureValues is not None :
            
            return{
                
                "chilli": {"time":latestMoistureValues[0][0],
                           "moisture": plant1Value},
                          
                "tomato":{"time":latestMoistureValues[1][0],
                           "moisture":plant2Value }
                
                
            }
        
        

class currentState(Resource):
    def __init__(self):
        pass

    def get(self):
        helper = currentMoistureValue()
        return helper.get()
#------------------------------------------------------------------------------

#----------------------------------- Tomato Plant ----------------------------------

class tomatoValue(object):

    def __init__(self):
        pass

    def get(self):
        
        database = r"sensor_data.db"

        # create a database connection
        conn = create_connection(database)
        print("---DB Connected")
        
        #plantName = list_all_tables(conn)
        
        moisturePlant1Values = select_all_Values(conn,'tomato')
       
        conn.close()
        if moisturePlant1Values is not None:
            return moisturePlant1Values
                
 
class tomato(Resource):
    def __init__(self):
        pass

    def get(self):
        helper = tomatoValue()
        return helper.get()
    
#------------------------------------------------------------------------------

#----------------------------------- Tomato Chilli----------------------------------

class tomatoPumpState(object):

    def __init__(self):
        pass

    def get(self):
        
        '''
        
        Pump At chilli Plant
        
        '''
        
        global pumpTomatoValue, client
        
        if(pumpTomatoValue == 0): 
            try:
                ret= client.publish("esp8266/tomato_sensor","PUMP_START") 
                print("=============>Starting Pump at tomato Plant")
                pumpTomatoValue = 1
            except:
                pass
        elif(pumpTomatoValue == 1):
            try:
                ret= client.publish("esp8266/tomato_sensor","PUMP_STOP") 
                print("=============>Starting Pump at tomato Plant")
                pumpTomatoValue = 0
            except:
                pass
        
        return "success"
        

class tomatoPump(Resource):
    def __init__(self):
        pass

    def get(self):
        helper = tomatoPumpState()
        return helper.get()
    
   


#------------------------------------------------------------------------------


#----------------------------------- Chilli Plant ----------------------------------

class chilliValue(object):

    def __init__(self):
        pass

    def get(self):
        
        database = r"sensor_data.db"

        # create a database connection
        conn = create_connection(database)
        print("---DB Connected")

        #plantName = list_all_tables(conn)
        
        moisturePlant2Values = select_all_Values(conn,'chilli')
       
        conn.close()
        if moisturePlant2Values is not None:
            return moisturePlant2Values
        
        
        

class chilli(Resource):
    def __init__(self):
        pass

    def get(self):
        helper = chilliValue()
        return helper.get()
    

#------------------------------------------------------------------------------


#----------------------------------- Pump Chilli----------------------------------

class chilliPumpState(object):

    def __init__(self):
        pass

    def get(self):
        
        '''
        
        Pump At chilli Plant
        
        '''
        global pumpChilliValue, client
        
        
        if(pumpChilliValue == 0):             
            try:
                ret= client.publish("esp8266/chilli_sensor","PUMP_START") 
                print("=============>Starting Pump at chilli Plant")
                pumpChilliValue = 1
            except exception as e:
                print(str(e))
                pass
            
        elif(pumpChilliValue == 1):
            try:
                ret= client.publish("esp8266/chilli_sensor","PUMP_STOP") 
                print("=============>Stoping Pump at chilli Plant")
                pumpChilliValue = 0
            except:
                pass
            
        
        return "success"

class chilliPump(Resource):
    def __init__(self):
        pass

    def get(self):
        helper = chilliPumpState()
        return helper.get()
    

#------------------------------------------------------------------------------


#------------------------ Url Links and related classes ---------------------------------------------

api.add_resource(currentState, "/")
api.add_resource(tomato, "/tomato")
api.add_resource(chilli, "/chilli")
api.add_resource(tomatoPump, "/tomato_pump")
api.add_resource(chilliPump, "/chilli_pump")




def main():
    
    global pumpChilliValue
    global pumpTomatoValue
    
    database = r"sensor_data.db"

    # create a database connection
    conn = create_connection(database)
    print("---DB Connected")
    
    with conn:
        
        print("===========>Start state of chilli and tomato Pump - set the value here from DB")
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name");

        rows = cur.fetchall()

        #for row in rows:
            #print(row[0])    
        
       
        #set the pump values from DB - i set it to 0
        
        
        pumpChilliValue = 0
        pumpTomatoValue = 0
    
    conn.close() 
    
    

def on_connect(client, userdata, flags, rc):
    pass

def on_message(client, userdata, msg):
    pass

if __name__ == "__main__":
    #main()
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set("pi", "password")
    client.connect("192.168.0.55", 1883, 60)
    app.run(host='192.168.0.55') #The IP of rasberry Pi

    
