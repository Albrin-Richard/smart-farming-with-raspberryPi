// Create a client instance
client = new Paho.MQTT.Client("192.168.0.55", 9001, "webpage" + new Date().getTime());

// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

// connect the client
client.connect({ userName: "", password: "", onSuccess: onConnect, onFailure: doFail });
var intervals = {'tomato' : "", 'chilli' : ""};
function pump_button_toggle() {
    var pump_name = ($(this).attr('id') == "tomato-pump-button") ? "esp8266/tomato_sensor" : "esp8266/chilli_sensor"; 
    var interval_key = ($(this).attr('id') == "tomato-pump-button") ? "tomato" : "chilli"; 
    if ($(this).attr('class') == "btn btn-success") {
        var i = 59;
        var element = $(this);
        intervals[interval_key] = setInterval(function () {
            if (i == 59) {
                element.removeClass('btn-success');
                element.addClass('btn-danger');
                turn_on_pump(pump_name);
            }
            if (i < 0) {
                clearInterval(intervals[interval_key]);
                turn_off_pump(pump_name);
                element.removeClass('btn-danger');
                element.addClass('btn-success');
                element.html('Turn on pump');
            }
            else {
                if (i >= 10) {
                    element.html('Turn off pump 0:' + (i--));
                }
                else {
                    element.html('Turn off pump 0:0' + (i--));
                }
            }

        }, 1000);

    }
    else {
        clearInterval(intervals[interval_key]);
        $(this).removeClass('btn-danger');
        $(this).addClass('btn-success');
        $(this).html('Turn on pump');
        turn_off_pump(pump_name);
    }
};

function turn_on_pump(pump_name) {
    msg = new Paho.MQTT.Message("PUMP_START");
    msg.destinationName = pump_name;
    client.send(msg);    
}

function turn_off_pump(pump_name) {
    msg = new Paho.MQTT.Message("PUMP_STOP");
    msg.destinationName = pump_name;
    client.send(msg);    
}

function map_range(value, low1, high1, low2, high2) {
    return low2 + (high2 - low2) * (value - low1) / (high1 - low1);
}

// called when the client connects
function onConnect() {
    // Once a connection has been made, make a subscription and send a message.
    console.log("onConnect");
    client.subscribe("esp8266/tomato");
    client.subscribe("esp8266/chilli");
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
    if (responseObject.errorCode !== 0) {
        console.log("onConnectionLost:" + responseObject.errorMessage);
    }
}

// called when the client loses its connection
function doFail(responseObject) {
    if (responseObject.errorCode !== 0) {
        console.log("onConnectionLost:" + responseObject.errorMessage);
    }
}

// called when a message arrives
function onMessageArrived(message) {
    if ((message.destinationName == "esp8266/chilli" || message.destinationName == "esp8266/tomato") && message.payloadString != "NOOP") {
        console.log(`for topic:${message.destinationName} onMessageArrived : ${message.payloadString}`);

        var element = message.destinationName == "esp8266/chilli" ? "#chilli-gague" : "#tomato-gague";
        $(element).data("percent", map_range(Number(message.payloadString), 900, 300, 0, 100));
        $(element).empty();
        $(element).gaugeMeter();

    }

}



var color_of_day = {}
function get_color_of_day(day) {
    if (!(day in color_of_day)) {
        color_of_day[day] = rand_color();
    }
    return color_of_day[day];
}

var generated_colors = new Set();
function rand_color() {
    var color;
    do {
        color = "#" + Math.floor(Math.random() * 16777215).toString(16);
    } while (generated_colors.has(color));
    return color;
}

$(document).ready(function () {
    $(".GaugeMeter").gaugeMeter();
    $.ajax({
        url: "http://192.168.0.55/index.php",
        method: "GET",
        success: function (xdata) {
            xdata = $.parseJSON(xdata);

            var chartColors = {
                red: 'rgb(255, 99, 132)',
                orange: 'rgb(255, 159, 64)',
                yellow: 'rgb(255, 205, 86)',
                green: 'rgb(75, 192, 192)',
                blue: 'rgb(54, 162, 235)',
                purple: 'rgb(153, 102, 255)',
                grey: 'rgb(231,233,237)'
            };
            console.log(xdata);

            var data = [xdata.tomato_data, xdata.chilli_data];
            var chartid = ["#tomato", "#chilli"];
            var daily_trends_charts = ["#tomato-trend", "#chilli-trend"];
            var colors = []
            $.each(data, function (index, value) {

                var time_stamp = [];
                var mlevel = [];
                var hourly_sum = 0;
                var num_readings_per_hour = 0;
                var last_hour = -1;
                var last_date = -1;
                var daily_trends = {};
                var hourly_readings = Array(24);
                for (var i in value) {
                    //console.log(data[i]);
                    let d = new Date(value[i].date_time)
                    let hour = d.getHours();
                    let date = (d.getMonth() + 1) + "/" + d.getDate();



                    if (last_hour != hour && last_hour != -1) {

                        time_stamp.push(date + " " + hour + ":00");

                        if(num_readings_per_hour == 0)
                        {
                            mlevel.push(mlevel[mlevel.length - 1]);
                        }
                        else
                        {
                            mlevel.push(map_range(hourly_sum / num_readings_per_hour, 900, 300, 0, 100));
                        }

                        if (last_date != date && last_date != -1) {
                            daily_trends[last_date] = hourly_readings;
                            hourly_readings = [, , , , , , , , , , , , , , , , , , , , , , ,];
                        }

                        hourly_readings[last_hour] = mlevel[mlevel.length - 1];

                        num_readings_per_hour = 0;
                        hourly_sum = 0;
                    } else {
                        hourly_sum += value[i].mositure_level;
                        num_readings_per_hour += 1;
                    }


                    last_hour = hour;
                    last_date = date;

                }

                var chartdata = {
                    labels: time_stamp,
                    datasets: [{
                        label: 'Moisture level',
                        borderColor: chartColors.blue,
                        backgroundColor: chartColors.blue,
                        data: mlevel
                    }]
                };

                var chartdata_daily = {
                    labels: ['0:00', '1:00', '2:00', '3:00', '4:00',
                        '5:00', '6:00', '7:00', '8:00', '9:00', '10:00',
                        '11:00', '12:00', '13:00', '14:00', '15:00',
                        '16:00', '17:00', '18:00', '19:00', '20:00',
                        '21:00', '22:00', '23:00'],
                    datasets: []
                };

                for (let day in daily_trends) {
                    color = get_color_of_day(day);
                    chartdata_daily.datasets.push({
                        label: 'Moisture level ' + day,
                        borderColor: color,
                        backgroundColor: color,
                        data: daily_trends[day]
                    })
                }

                var ctx = $(chartid[index]);

                var Graph = new Chart(ctx, {
                    type: 'line',
                    data: chartdata
                });
                var trend_ctx = $(daily_trends_charts[index]);
                var Graph = new Chart(trend_ctx, {
                    type: 'line',
                    data: chartdata_daily
                });

            });
            latest_tomato_moisture_level = map_range(xdata.tomato_data[xdata.tomato_data.length - 1].mositure_level, 900, 300, 0, 100);
            latest_chilli_moisture_level = map_range(xdata.chilli_data[xdata.chilli_data.length - 1].mositure_level, 900, 300, 0, 100);

            $("#chilli-gague").data("percent", latest_chilli_moisture_level);
            $("#chilli-gague").empty();
            $("#chilli-gague").gaugeMeter();
            $("#tomato-gague").data("percent", latest_tomato_moisture_level);
            $("#tomato-gague").empty();
            $("#tomato-gague").gaugeMeter();

            //console.log(time_stamp);
            //console.log(mlevel);
        },
        error: function (data) {
            console.log("failed")
            console.log(data);
        }
    });
});