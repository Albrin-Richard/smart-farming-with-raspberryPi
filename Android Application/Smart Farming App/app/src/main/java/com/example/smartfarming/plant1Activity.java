package com.example.smartfarming;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.*;

import androidx.appcompat.app.AppCompatActivity;

import android.app.ProgressDialog;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.widget.Button;
import android.widget.TextView;

import com.jjoe64.graphview.DefaultLabelFormatter;
import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.GridLabelRenderer;
import com.jjoe64.graphview.LegendRenderer;
import com.jjoe64.graphview.helper.DateAsXAxisLabelFormatter;
import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.series.LineGraphSeries;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;


public class plant1Activity extends AppCompatActivity {
    private static String LOG_CLICK = "UI_ELEMENT_BUTTON_CLICK";

    Handler mainHandler = new Handler();
    ProgressDialog progressDialog;
    String linkValue,  link="";
    String linkPump = "";
    TextView pumpChilli;
    int pumpState;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_plant1);

        pumpChilli = (TextView) findViewById(R.id.pump1State);

        //To get link from previous page
        Intent intentPlant1 = getIntent();
        link = intentPlant1.getStringExtra("link");

        if(intentPlant1 !=null) {
            linkValue = link +"chilli";
            System.out.println(linkValue);
            linkPump = link +"chilli_pump";
        }

        //new Thread
        new fetchData().start();

        Button button = (Button) findViewById(R.id.button);


        button.setOnClickListener(v -> {

            if (pumpState == 0){
                pumpChilli.setText("ON");
                pumpChilli.setBackgroundColor(Color.GREEN);
                pumpState = 1;
                button.setText("STOP PUMP");

            }else if(pumpState == 1){
                pumpChilli.setText("OFF");
                pumpChilli.setBackgroundColor(Color.RED);
                pumpState = 0;
                button.setText("START PUMP");
            }
            //new Thread
            new fetchPump().start();
            Log.i(LOG_CLICK, "--->Chilli Pump Button Click");

        });

    }


    protected void setGraphValues(String jsonString) throws JSONException {

        // Parse the JSON String
        JSONObject jsonObject = new JSONObject(jsonString);
        JSONObject jsonobject = jsonObject.getJSONObject("chilli");

        //Set Pump Value and Background color
        if (jsonObject.getInt("pump_chilli") == 1){
            pumpChilli.setText("ON");
            pumpChilli.setBackgroundColor(Color.GREEN);
            pumpState = 1;

        }else {
            pumpChilli.setText("OFF");
            pumpChilli.setBackgroundColor(Color.RED);
            pumpState = 0;
        }

        SimpleDateFormat format;
        Date date = null;
        GraphView graph = (GraphView) findViewById(R.id.graph1);
        LineGraphSeries<DataPoint> series = new LineGraphSeries<DataPoint>();

        for(int idx = 0; idx<jsonobject.length(); idx++){
            //Log.e(LOG_CLICK, "Key = " + jsonobject.names().getString(idx) + " value = " + jsonobject.get(jsonobject.names().getString(idx)));
            String key = jsonobject.names().getString(idx);
            format = new SimpleDateFormat("MM-dd-yy");

            try {
                date = format.parse(key);
                //System.out.println(date);
            } catch (ParseException e) {
                e.printStackTrace();
            }

            JSONArray dateValue = jsonobject.getJSONArray(key);

            for (int i=0;i<dateValue.length();i++) {

                date.setHours(dateValue.getJSONArray(i).getInt(0));
                //System.out.println(date);
                series.appendData(new DataPoint(date, dateValue.getJSONArray(i).getInt(1)), true,10*24);
            }
        }

        series.setColor(Color.rgb(0,80,100)); //set Color
        series.setTitle("Chilli"); // set Title
        series.setDrawDataPoints(true); // Draw Data Points
        series.setThickness(2); //set Thickness of Line

        graph.addSeries(series);

        //X axis date-format
        DateFormat df = new SimpleDateFormat("MM/dd 'H':HH");
        graph.getGridLabelRenderer().setLabelFormatter(new DateAsXAxisLabelFormatter(getApplicationContext(), df));
        graph.getGridLabelRenderer().setHorizontalLabelsAngle(50);

        //Legend on Top Right
        graph.getLegendRenderer().setVisible(true);
        graph.getLegendRenderer().setAlign(LegendRenderer.LegendAlign.TOP);

        //Horizontal and Vertical axis Labels
        GridLabelRenderer gridLabel = graph.getGridLabelRenderer();
        gridLabel.setHorizontalAxisTitle("Date and Time");
        gridLabel.setVerticalAxisTitle("Moisture Level");


        // activate horizontal zooming and scrolling
        graph.getViewport().setScalable(true);
        // activate horizontal scrolling
        graph.getViewport().setScrollable(true);
        // activate horizontal and vertical zooming and scrolling
        graph.getViewport().setScalableY(true);
        // activate vertical scrolling
        graph.getViewport().setScrollableY(true);



        // set date label formatter
        //graph.getGridLabelRenderer().setNumHorizontalLabels(4); // only 4 because of the space

        // set manual x bounds to have nice steps
        //graph.getViewport().setMinX(d1.getTime());
        //System.out.println("-->Date Max"+date);
        //graph.getViewport().setMaxX(date.getTime());
        graph.getViewport().setXAxisBoundsManual(true);


        // as we use dates as labels, the human rounding to nice readable numbers
        // is not necessary
        graph.getGridLabelRenderer().setHumanRounding(true);



        // set manual Y bounds
        //graph.getViewport().setYAxisBoundsManual(true);
        //graph.getViewport().setMinY(0);
        //graph.getViewport().setMaxY(100);


    }

    class fetchData extends Thread{

        String jsonData = "";
        @Override
        public  void run(){

            // FETCHING DATA msg to show
            mainHandler.post(new Runnable() {
                @Override
                public void run() {

                    progressDialog = new ProgressDialog(plant1Activity.this);
                    progressDialog.setMessage("Fetching Data");
                    progressDialog.setCancelable(false);
                    progressDialog.show();

                }
            });

            try {
                URL url = new URL(linkValue);
                HttpURLConnection httpURLConnection = (HttpURLConnection) url.openConnection();
                InputStream inputStream = httpURLConnection.getInputStream();
                BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));

                String line;

                while ((line = bufferedReader.readLine()) != null){
                    jsonData = jsonData + line;
                }

                if(!jsonData.isEmpty()){

                    //jsonString = data;
                    Log.i(LOG_CLICK, "--->data got plant1");


                }

                httpURLConnection.disconnect();

            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }

            // FETCHING DATA msg to disappear
            mainHandler.post(new Runnable() {
                @Override
                public void run() {

                    if(progressDialog.isShowing()){
                        progressDialog.dismiss();
                    }

                    // To Update Plants Value
                    try {
                        setGraphValues(jsonData);
                        Log.i(LOG_CLICK, "--->Set Moisture");
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }


                }
            });

        }


    }

    class fetchPump extends Thread{

        String jsonData = "";
        @Override
        public  void run(){

            // FETCHING DATA msg to show
            mainHandler.post(new Runnable() {
                @Override
                public void run() {

                    progressDialog = new ProgressDialog(plant1Activity.this);
                    progressDialog.setMessage("Starting Pump");
                    progressDialog.setCancelable(false);
                    progressDialog.show();

                }
            });

            try {
                URL url = new URL(linkPump);
                HttpURLConnection httpURLConnection = (HttpURLConnection) url.openConnection();
                InputStream inputStream = httpURLConnection.getInputStream();
                /*BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));

                String line;

                while ((line = bufferedReader.readLine()) == null){
                    jsonData = jsonData + line;
                }

                if(jsonData.isEmpty()){

                    //jsonString = data;
                    Log.i(LOG_CLICK, "--->data got Chilli Pump");


                }*/

                httpURLConnection.disconnect();

            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }

            // FETCHING DATA msg to disappear
            mainHandler.post(new Runnable() {
                @Override
                public void run() {

                    if(progressDialog.isShowing()){
                        progressDialog.dismiss();
                    }

                    // To Update Plants Value
                    try {
                        setGraphValues(jsonData);
                        Log.i(LOG_CLICK, "--->Set Moisture");
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }


                }
            });

        }


    }
}