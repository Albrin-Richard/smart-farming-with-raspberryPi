<?php
    $db = new SQLite3('/home/pi/Documents/Anastasiya/IOT_project/sensor_data.db');

    $res = $db->query("SELECT * from tomato");// WHERE (date_time BETWEEN '2022-05-01T01:51:27' AND '2022-05-01T02:07:28')");

    $tomato_data = array();
    while ($row = $res->fetchArray(SQLITE3_ASSOC)) {
        array_push($tomato_data, $row);
    }

    $res = $db->query("SELECT * from chilli");// WHERE (date_time BETWEEN '2022-05-01T01:51:27' AND '2022-05-01T02:07:28')");

    $chilli_data = array();
    while ($row = $res->fetchArray(SQLITE3_ASSOC)) {
        array_push($chilli_data, $row);
    }
    
    $data = [
        'tomato_data' => $tomato_data,
        'chilli_data' => $chilli_data,
    ];

    print json_encode($data);
?>