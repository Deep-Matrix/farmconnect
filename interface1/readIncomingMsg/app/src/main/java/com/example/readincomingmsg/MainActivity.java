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
    public final String ngrokID="894e346f";
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
    public void messageReceived(final String senderPhoneNumber, String emailFrom, String emailBody, String msgBody, long timeStamp, String Message) {
        Log.d("msgInfo",senderPhoneNumber);
        Log.d("msgInfo",Message);


        String msg="";
        msg=Message.replaceAll(" "," ");
        msg=msg.replaceAll("\n","\n");


        Log.d("ABC",msg);

        numFaarm=senderPhoneNumber;
        msgFarm=msg;


        Toast.makeText(this, "readIncomingMsg!: " + msg, Toast.LENGTH_SHORT).show();


        RequestQueue MyRequestQueue = Volley.newRequestQueue(getApplicationContext());
        String url = "https://"+ngrokID+".ngrok.io/";
        final String finalMsg = msg;

        StringRequest MyStringRequest = new StringRequest(Request.Method.POST, url, new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {
                //This code is executed if the server responds, whether or not the response contains data.
                //The String 'response' contains the server's response.
            }
        }, new Response.ErrorListener() { //Create an error listener to handle errors appropriately.
            @Override
            public void onErrorResponse(VolleyError error) {
                //This code is executed if there is an error.
            }
        }) {
            protected Map<String, String> getParams() {
                Map<String, String> MyData = new HashMap<String, String>();
                MyData.put("phone_no", senderPhoneNumber); //Add the data you'd like to send to the server.
                MyData.put("details", finalMsg); //Add the data you'd like to send to the server.
                return MyData;
            }
        };
        MyRequestQueue.add(MyStringRequest);

        //

    }



}

