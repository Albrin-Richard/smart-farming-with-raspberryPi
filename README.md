# Smart farming with Raspberry pi
Course project for CSC275 (CSUS).

This repo is organized as below
```bash
├── node_mcu_code               #Code that is uploaded to NODE-MCU(ESP8266)
│   ├── chilli-esp8266
│   │   └── chilli-esp8266.ino  #Code that is uploaded to NODE-MCU(ESP8266) in chilli pot
│   └── tomato-esp8266
│       └── tomato-esp8266.ino  #Code that is uploaded to NODE-MCU(ESP8266) in tomato pot
├── python_mqtt_client 
│   └── mqtt_client.py          #MQTT python client that is running on raspberry-pi and listening to messages from Nodes
├── README.md
└── webserver                   #All files that are responsible for creating Web dashboard
    ├── bootstrap.min.css       #CSS downloaded from web (Not claiming ownership)
    ├── chilli.jpeg             #Jpeg downloaded from web (Not claiming ownership)
    ├── index.html
    ├── index.php
    ├── js
    │   ├── app.js
    │   ├── bootstrap.js        #JS Library downloaded from web (Not claiming ownership)
    │   ├── chart.js            #JS Library downloaded from web (Not claiming ownership)
    │   ├── GaugeMeter.js       #JS Library downloaded from web (Not claiming ownership)
    │   ├── jquery.js           #JS Library downloaded from web (Not claiming ownership)
    │   ├── mqtt.js             #JS Library downloaded from web (Not claiming ownership)
    │   └── popper.min.js       #JS Library downloaded from web (Not claiming ownership)
    └── tomato.jpeg             #Jpeg downloaded from web (Not claiming ownership)
```

Programs installed on Raspberry-PI:

```bash
   sudo apt-get install mosquitto
   sudo apt-get install mosquitto-clients
   sudo pip install paho-mqtt
   sudo apt install sqlite3
   sudo apt install apache2
   sudo apt-get install php7.4
```

Programs needed for uploding code onto NODE-MCU(ESP8266) :
[ArduinoIDE](https://www.arduino.cc/en/software)
## Equipment used in this project

|Name           | Item                                              | Quantity      |
|---------------|---------------------------------------------------| ------------- |
|Raspberry Pi 2 | <img src="./images/Raspi.png" width="100">                    | 1 |
|5v Relay       | <img src="./images/Relay.png" width="100">                    | 2 |
|Esp8266        | <img src="./images/Esp8266.png" width="80">                   | 2 |
|Breadboard     | <img src="./images/Breadboard.png" width="80">                | 2 |
|9V battery     | <img src="./images/9vbttery.png" width="100">                 | 2 |
|5v DC waterpump| <img src="./images/waterpump.png" width="100">                | 2 |
|Soil moisture sensor| <img src="./images/SoilMoistureSensor.png" width="100">       | 2 |



## Circuit diagram for NodeMCU
<img src="./images/circuit.png" width="500">

## Web Dashboard

### Home page
<img src="./images/webdash.gif" width="800">

### Current moisture levels
<img src="./images/current-m-levels.gif" width="800">

### Pump turn on/off, with timer
<img src="./images/pump-on-off.gif" width="800">

## Flask Server Log
<img src="./images/serverLog.png" width="500">

## Android Application

### Dashboard page
<img src="./images/dashboard.png" height="400">

### Chilli plant page
<img src="./images/chilliGraph.png" height="400">

### Dashboard page
<img src="./images/tomatoGraph.png" height="400">

## Video demonstration of project and its working

+ Youtube video link here [CS275 Project presentation](https://www.youtube.com/watch?v=5ltGwt-I5Is)
