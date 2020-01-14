package com.example.readincomingmsg;

import android.content.Intent;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
//import android.support.v7.app.AppCompatActivity;
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

    TextView text;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        //Register sms listener

        text=findViewById(R.id.text);

        MessageReceiver.bindListener(this);


    }

    @Override
    public void messageReceived(String senderPhoneNumber,String emailFrom,String emailBody,String msgBody,long timeStamp,String Message) {
        Log.d("msgInfo",senderPhoneNumber);
        Log.d("msgInfo",Message);
        String message=senderPhoneNumber+" : "+Message;
        //
        String u=" https://b8601c8e.ngrok.io/hello/"+senderPhoneNumber+"/"+Message;
//        Intent viewIntent =
//                new Intent("android.intent.action.VIEW",
//                        Uri.parse(u));
//        startActivity(viewIntent);

//        try {
//            new URL(u).openStream();
//        } catch (IOException e) {
//            Log.d("errr",e.toString());
//            e.printStackTrace();
//        }


//working...geting from json data
//        RequestQueue requestQueue;
//        requestQueue= Volley.newRequestQueue(MainActivity.this);
//
//        JsonObjectRequest jsonObjectRequest=new JsonObjectRequest(Request.Method.GET,
//                "https://b8601c8e.ngrok.io/hello",null,new Response.Listener<JSONObject>(){
//            @Override
//            public void onResponse(JSONObject response) {
//                try {
//                    Log.d("myapp","The response is : "+response.getString("title"));
//                    text.setText(response.getString("message"));
//                } catch (JSONException e) {
//                    e.printStackTrace();
//                }
//            }
//        },new Response.ErrorListener(){
//            @Override
//            public void onErrorResponse(VolleyError error) {
//                Log.d("myapp","Something wentt wrong");
//                text.setText("Soething went Wrong");
//            }
//        });
//        requestQueue.add(jsonObjectRequest);
//end

//        final String url = "https://b8601c8e.ngrok.io/hello/"+senderPhoneNumber;
//
//// prepare the Request
//        RequestQueue requestQueue;
//        requestQueue= Volley.newRequestQueue(MainActivity.this);
//        JsonObjectRequest getRequest = new JsonObjectRequest(Request.Method.GET, url, null,
//                new Response.Listener<JSONObject>()
//                {
//                    @Override
//                    public void onResponse(JSONObject response) {
//                        // display response
//                        Log.d("ABC", response.toString());
//                    }
//                },
//                new Response.ErrorListener()
//                {
//                    @Override
//                    public void onErrorResponse(VolleyError error) {
//                        Log.d("ABC", "errrorrr123");
//                    }
//                }
//        );
//
//// add it to the RequestQueue
//        requestQueue.add(getRequest);
        //



        //


        //
        String msg="";
        msg=Message.replaceAll(" ","%20");
        msg=msg.replaceAll("\n","%0A");

//        }
        Log.d("ABC",msg);


        Toast.makeText(this, "readIncomingMsg!: " + msg, Toast.LENGTH_SHORT).show();
        MyTask t1 = new MyTask();
        t1.execute("https://b8601c8e.ngrok.io/hello/"+senderPhoneNumber+"/"+msg);

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
                        String title = "title hereeee";
                        String year = "year hereeee";
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
            text.setText(searchResult);
        }
    }


}

