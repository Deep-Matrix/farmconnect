package com.example.readincomingmsg;

import android.content.Intent;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
//import android.support.v7.app.AppCompatActivity;
import android.telephony.SmsManager;
import android.util.Log;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.AuthFailureError;
import com.android.volley.NetworkResponse;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.VolleyLog;
import com.android.volley.toolbox.HttpHeaderParser;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity implements MessageListener {

    TextView text1;
    TextView text2;
    public final String ngrokID="3a6c7657";
    public String numFaarm;
    public String msgFarm;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        //Register sms listener

        text1=findViewById(R.id.text1);
        text2=findViewById(R.id.text2);

        MessageReceiver.bindListener(this);


    }

    @Override
    public void messageReceived(String senderPhoneNumber,String emailFrom,String emailBody,String msgBody,long timeStamp,String Message) {
        Log.d("msgInfo",senderPhoneNumber);
        Log.d("msgInfo",Message);


        String msg="";
        msg=Message.replaceAll(" ","%20");
        msg=msg.replaceAll("\n","%0A");


        Log.d("ABC",msg);

        numFaarm=senderPhoneNumber;
        msgFarm=msg;


        Toast.makeText(this, "readIncomingMsg!: " + msg, Toast.LENGTH_SHORT).show();
        MyTask t1 = new MyTask();
        t1.execute("https://"+ngrokID+".ngrok.io/post?phno="+senderPhoneNumber+"&msg="+msg);

    }



    class MyTask extends AsyncTask<String, Void, String>{
        String searchResult = "";
        String jsonString = "";
        String line = "";

        @Override
        protected String doInBackground(String... strings) {
            URL url = null;
            try {
                url = new URL(strings[0]);
                HttpURLConnection con = (HttpURLConnection) url.openConnection();
                con.connect();
                InputStream inputStreamReader = con.getInputStream();
                BufferedReader reader = new BufferedReader(new InputStreamReader(inputStreamReader));

                while((line = reader.readLine()) != null){
                    jsonString += line + "\n";
                }
                if(jsonString != null){
                    JSONObject jsonObject = new JSONObject(jsonString);
                    JSONArray jsonArray = jsonObject.getJSONArray("Search");
                    for(int i = 0; i < jsonArray.length() ; i++){
                        JSONObject movie = jsonArray.getJSONObject(i);
                        String title = "ttt";
                        String year = "yyyyyyy";
                        searchResult += title + " " + year + "\n";
                    }
                }

            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            } catch (JSONException e) {
                e.printStackTrace();
            }
            return searchResult;

        }

        @Override
        protected void onPostExecute(String s) {
            super.onPostExecute(s);
            text1.setText(msgFarm);
            text2.setText(numFaarm);
        }
    }



}

