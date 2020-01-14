package com.example.readincomingmsg;

import android.os.Bundle;
//import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity implements MessageListener {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        //Register sms listener
        MessageReceiver.bindListener(this);
    }

    @Override
    public void messageReceived(String senderPhoneNumber,String emailFrom,String emailBody,String msgBody,long timeStamp,String Message) {
        Log.d("msgInfo",senderPhoneNumber);
        Log.d("msgInfo",Message);
        String message=senderPhoneNumber+" : "+Message;
        Toast.makeText(this, "readIncomingMsg!: " + message, Toast.LENGTH_SHORT).show();
    }
}
