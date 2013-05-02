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

int width = 220;
int height = 360;
float theScale = 1;

int segmentCount = 0;
int maxAnimation = 60;
int frames = 30;

PFont font;

boolean firstDraw = true;

int count = 0; 

int colorCounter = 0;

int[] colors = new int[4];

int the_color = color(255,0,0);

PrintWriter logger;

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
 
 font = loadFont("HelveticaNeue-CondensedBold-80.vlw");
 
  //colour choices - https://kuler.adobe.com/#themeID/2362707
colors[0] = color(0,161,154);
colors[1] = color(4,191,157);
colors[2] = color(242,232,92);
colors[3] = color(245,61,84);
 
 m = new MQTTLib(MQTT_BROKER, new MessageHandler());
 m.connect(CLIENT_ID, CLEAN_START, KEEP_ALIVE);
 m.subscribe(TOPICS, QOS);
 
 logger = createWriter(year() + "-" + month()  + "-" + day() + "/" + hour() + "_" + minute() + "_log.txt");

 
}

public void draw(){

  background(39,39,38);
  smooth();
  //stroke(210, 123, 34);
  fill(the_color);
  textFont(font, 80);
  textAlign(CENTER);
  text(str(count), ((width/2)), (height/2));
        
  }

public void keyPressed() {

    createSmile();
}



public void createSmile(){
    count++;
    
    colorCounter++;
       if (colorCounter == colors.length){
           colorCounter = 0;
       }
    
       the_color = colors[colorCounter];
       
   logger.println(hour() + ":" + minute() + ":" + second() + "." + millis());
   logger.flush();
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

public void stop() {
  logger.close();
  super.stop();
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
