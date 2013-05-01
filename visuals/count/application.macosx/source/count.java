import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import com.ibm.mqtt.MqttClient; 
import com.ibm.mqtt.MqttSimpleCallback; 
import com.ibm.mqtt.MqttException; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class count extends PApplet {

int width = 300;
int height = 300;
float theScale = 1;

int segmentCount = 0;
int maxAnimation = 60;
int frames = 30;

PFont font;

boolean firstDraw = true;

int count = 0; 

//MQTT Parameters
private MQTTLib m;
private String MQTT_BROKER ="tcp://localhost:1883";
private String CLIENT_ID = "Processing-Count";
private int[] QOS = {1};
private String[] TOPICS = {"smiles"};
private boolean CLEAN_START = true;
private short KEEP_ALIVE = 30;


public void setup(){

 size(width, height);
 background(0);
 frameRate(frames);
 
 font = loadFont("HelveticaNeue-Light-72.vlw");
 

 
 m = new MQTTLib(MQTT_BROKER, new MessageHandler());
 m.connect(CLIENT_ID, CLEAN_START, KEEP_ALIVE);
 m.subscribe(TOPICS, QOS);

 
}

public void draw(){

  background(39,39,38);
  //stroke(210, 123, 34);
  textFont(font, 72);
  textAlign(CENTER);
  text(str(count), ((width/2)), (height/2));
        
  }

public void keyPressed() {

    createSmile();
}



public void createSmile(){
    count++;
}

private class MessageHandler implements MqttSimpleCallback {
public void connectionLost() throws Exception {
 System.out.println( "Connection has been lost." );
 //do something here
 }
public void publishArrived( String topicName, byte[] payload, int QoS, boolean retained ){
 String s = new String(payload);
 //Display the string
 createSmile();
 } 

 }





 public class MQTTLib {
 private MqttSimpleCallback callback;
 private MqttClient client = null;

 MQTTLib(String broker, MqttSimpleCallback p) {
 callback = p;
 try {
 client = (MqttClient) MqttClient.createMqttClient(broker, null);
 //class to call on disconnect or data received
 client.registerSimpleHandler(callback);
 } catch (MqttException e) {
 System.out.println( e.getMessage() );
 }
 }

 public boolean connect(String client_id, boolean clean_start, short keep_alive) {

 try {
 //connect - clean_start=true drops all subscriptions, keep-alive is the heart-beat
 client.connect(client_id, clean_start, keep_alive);
 print("connected");
 //subscribe to TOPIC
 return true;
 } catch (MqttException e) {
 System.out.println( e.getMessage() );
 return false;
 }
 }

 public boolean subscribe(String[] topics, int[] qos ) {
 try {
 //subscribe to TOPIC
 client.subscribe(topics, qos);
 return true;
 } catch (MqttException e) {
 System.out.println( e.getMessage() );
 return false;
 }
 }

}
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "count" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
