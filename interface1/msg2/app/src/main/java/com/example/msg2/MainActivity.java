package com.example.msg2;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.widget.Toast;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class MainActivity extends AppCompatActivity {

    public static final String OTP_REGEX = "[0-9]{1,6}";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        SmsReceiver.bindListener(new SmsListener() {
            @Override
            public void messageReceived(String messageText) {

                //From the received text string you may do string operations to get the required OTP
                //It depends on your SMS format
                Log.d("msgg",messageText);
                Toast.makeText(MainActivity.this,"Message: "+messageText,Toast.LENGTH_LONG).show();







            }
        });
    }
}
