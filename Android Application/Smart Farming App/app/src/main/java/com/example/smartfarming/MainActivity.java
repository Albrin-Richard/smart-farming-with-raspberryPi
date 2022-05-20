package com.example.smartfarming;

import androidx.appcompat.app.AppCompatActivity;

import android.app.ProgressDialog;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.widget.*;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.*;
import java.net.*;

public class MainActivity extends AppCompatActivity {
    private static String LOG_CLICK = "UI_ELEMENT_BUTTON_CLICK";


    Handler mainHandler = new Handler();
    ProgressDialog progressDialog;
    String linkValue = "";
    TextView plant1Value, plant2Value;
    EditText link;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        plant1Value = (TextView) findViewById(R.id.plant1MoistureValue);
        plant2Value = (TextView) findViewById(R.id.plant2MoistureValue);


        link = (EditText) findViewById(R.id.urlTextEdit);

        Button button = (Button) findViewById(R.id.button);

        button.setOnClickListener(v -> {

            linkValue = String.valueOf(link.getText());

            // Fetch Data From Server
            new fetchData().start();
            Log.i(LOG_CLICK, "--->Button Click");

        });




    }

    protected void setMoisture(String jsonString) throws JSONException {

        JSONObject plant1JsonValue, plant2JsonValue;
        JSONObject jsonObject = new JSONObject(jsonString);

        plant1JsonValue = jsonObject.getJSONObject("chilli");
        plant2JsonValue = jsonObject.getJSONObject("tomato");

        //Set Plant 1 Value and Background color
        if (plant1JsonValue.getInt("moisture") >= 50){
            plant1Value.setText(plant1JsonValue.getString("moisture"));
            plant1Value.setBackgroundColor(Color.GREEN);
        }else {
            plant1Value.setText(plant1JsonValue.getString("moisture"));
            plant1Value.setBackgroundColor(Color.RED);
        }

        //Set Plant 2 Value and Background color
        if (plant2JsonValue.getInt("moisture") >= 50){
            plant2Value.setText(plant2JsonValue.getString("moisture"));
            plant2Value.setBackgroundColor(Color.GREEN);
        }else {
            plant2Value.setText(plant2JsonValue.getString("moisture"));
            plant2Value.setBackgroundColor(Color.RED);
        }






    }


    class fetchData extends Thread{

        String jsonData = "";
        @Override
        public  void run(){

            // FETCHING DATA msg to show
            mainHandler.post(new Runnable() {
                @Override
                public void run() {

                    progressDialog = new ProgressDialog(MainActivity.this);
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
                    Log.i(LOG_CLICK, "--->data got");


                }



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
                        setMoisture(jsonData);
                        Log.i(LOG_CLICK, "--->Set Moisture");
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }



                }
            });

        }
    }

    public void openPlant1Activity (View view){
        Intent intent = new Intent(this,plant1Activity.class);
        //Send link value to other two activities
        intent.putExtra("link", linkValue);
        startActivity(intent);
    }

    public void openPlant2Activity (View view){
        Intent intent = new Intent(this,plant2.class);
        //Send link value to other two activities
        intent.putExtra("link", linkValue);
        startActivity(intent);
    }
}