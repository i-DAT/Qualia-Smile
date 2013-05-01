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

public class smile extends PApplet {

ArrayList smiles;
ArrayList triangles;

int width = 900;
int height = 360;
float theScale = 1;

int segmentCount = 0;
int maxAnimation = 60;
int frames = 30;

PFont font;

boolean firstDraw = true;

int colorCounter = 0;

int[] colors = new int[4];

//MQTT Parameters
private MQTTLib m;
private String MQTT_BROKER ="tcp://localhost:1883";
private String CLIENT_ID = "TestProcessing";
private int[] QOS = {1};
private String[] TOPICS = {"smiles"};
private boolean CLEAN_START = true;
private short KEEP_ALIVE = 30;





public void setup(){

 size(width, height);
 background(0);
 frameRate(frames);
 
 font = loadFont("HelveticaNeue-Light-48.vlw");
 
 smiles = new ArrayList();
 
 m = new MQTTLib(MQTT_BROKER, new MessageHandler());
 m.connect(CLIENT_ID, CLEAN_START, KEEP_ALIVE);
 m.subscribe(TOPICS, QOS);
 
 //l1.init(100,200);
 //smiles.add(new SmileLine(100,200,100));
 
 //mqtt = new MQTT( this );
 //#mqtt.connect( "127.0.0.1", 1883, "mqtt_receiver" );
 //mqtt.DEBUG = true;
 //mqtt.subscribe("aSmile","gotSmile");
 
  //colour choices - https://kuler.adobe.com/#themeID/2362707
colors[0] = color(0,161,154);
colors[1] = color(4,191,157);
colors[2] = color(242,232,92);
colors[3] = color(245,61,84);
 
 
 triangles = new ArrayList();
 //triangles.add(new SmileTriangle(100,100));
 triangles.add(new SmileTriangle());
 
 
 


}

public void draw(){
  //if (firstDraw == true){
    //mqtt.subscribe("smiles","gotSmile");
    firstDraw = false;
  //}
  scale(theScale);
  //translate(50,height/2);
  background(39,39,38);
  smooth();

  //text("Qualia-Smile", 15, 60); 

  //l1.update();
  //l1.addSmile();
  
  //loop through and display
  /*for(int i = 1; i <= smiles.size(); i++){
    SmileLine smile = (SmileLine) smiles.get(i - 1);
    smile.update();
  }*/
  
  for(int i = 1; i <= triangles.size(); i++){
    SmileTriangle smile = (SmileTriangle) triangles.get(i - 1);
    smile.draw();
    
    if((i == triangles.size()) && (segmentCount < maxAnimation)){
        //smile.update();
        //if(segmentCount < 24){
            segmentCount++;
            //println(segmentCount);
            smile.drawSegment(segmentCount);
            //textFont(font, 32);
            //text("harvesting", (width/2) - 200, (height/2) - 200);
            //stroke(255,255,255,127);
            noStroke();
            fill(255,255,255,(255 - ((255/maxAnimation)*segmentCount)));
            rect(0, 0, width, height);
            
        //}
    }
        
        
  }
  
  //test sin wave
/*float a = 0.0;
float inc = TWO_PI/25.0;
float prev_x = 0, prev_y = 50, x, y;

for(int i=0; i<=width; i=i+4) {
  x = i;
  y = 50 + sin(a) * 40.0;
  line(prev_x, prev_y, x, y);
  prev_x = x;
  prev_y = y;
  a = a + inc;
}*/
  
  
}

public void keyPressed() {
    //SmileLine smile = (SmileLine) smiles.get(smiles.size()-1);
    //smile.addSmile();
    
    createSmile();
    
    //theScale = theScale - 0.01;
     //mqtt.subscribe("smiles","gotSmile");
}

/*void gotSmile(MQTTMessage msg){
  createSmile();
  
  println( msg.toString() );
  println( new String(msg.payload) );
}*/

public void aSmile(byte[] payload){

  
  createSmile();
  
}

public void createSmile(){
    SmileTriangle tri = (SmileTriangle) triangles.get(triangles.size()-1);
    tri.addAlignedTriangle();
    segmentCount = 0;
}

class SmileTriangle {
    PVector pointA, pointB, pointC;
    int r,g,b;
    int the_color;
    SmileTriangle(){
        int div = (height/2) - 50; 
        pointA = new PVector(200,div);
        pointB = new PVector(300,((div) +100));
        pointC = new PVector(100,((div) +100));
        
         //use colors from Nathan's design
       
       r = 240;
       g = 240;
       b = 239;
       the_color = color(r,g,b);
        
      
    }
    SmileTriangle(int x, int y){
        pointA = new PVector(x,y);
        pointB = new PVector(x+100,y+100);
        pointC = new PVector(x+PApplet.parseInt(random(100)),y+PApplet.parseInt(random(100)));
        
        //use colors from Nathan's design
       r = 240;
       g = 240;
       b = 239;
       the_color = color(r,g,b);  
    }
    SmileTriangle(int aX, int aY, int bX, int bY){
        pointA = new PVector(aX,aY);
        pointB = new PVector(bX,bY);
        pointC = new PVector(constrain(bX+PApplet.parseInt(random(-100,100)),0,width),constrain(PApplet.parseInt(bY+random(-100,100)),0,height));
        
        //use colors from Nathan's design
       //r = 240;
       //g = 240;
       //b = 239;
       
       //r = int(random(215,255));
       //r = int(random(180,255));
       //g = int(random(180,255));
       //b = int(random(180,255));
       
       colorCounter++;
       if (colorCounter == colors.length){
           colorCounter = 0;
       }
    
       the_color = colors[colorCounter];
    }
    public void _setColors(){
        stroke(the_color);
        fill(the_color);
        strokeWeight(1);
    }
    public void draw(){
        _setColors();
        triangle(pointA.x,pointA.y,pointB.x,pointB.y,pointC.x,pointC.y);
    }
    public void drawSegment(int count){
        _setColors();
        //int xTo = int((pointC.x / count) - pointB.x);
        //int yTo = int((pointC.y / count) - pointB.y);
        //int xTo = int((pointC.x / count));
        //int yTo = int((pointC.y / count));
        PVector to = new PVector();
        //PVector to2 = new PVector();
        //to1.sub(pointA,pointC);
        //to2.sub(pointB,pointC);
        //int xTo = int((pointC.x / count));
        //int yTo = int((pointC.y / count));
        float change =(PApplet.parseFloat(count)/PApplet.parseFloat(maxAnimation));
        to = PVector.lerp(pointB,pointC,change);
        //println(change);
        //print(to);
        triangle(pointA.x,pointA.y,pointB.x,pointB.y,to.x,to.y);
        //line(pointA.x,pointA.y,to1.x,to1.y);
        //line(pointB.x,pointB.y,to2.x,to2.y);
    }
    public void addTriangle(){
      triangles.add(new SmileTriangle(PApplet.parseInt(pointC.x),PApplet.parseInt(pointC.y)));
    }
    public void addAlignedTriangle(){
      triangles.add(new SmileTriangle(PApplet.parseInt(pointB.x),PApplet.parseInt(pointB.y),PApplet.parseInt(pointC.x),PApplet.parseInt(pointC.y)));
    }
    
}

class SmileLine {
  int x1,y1,z1,x2,y2,z2,angle,r,g,b;
  
  //PVector start
  //direction of line gen. True = +ve
  boolean xD, yD;
  SmileLine(int xA,int yA,int intensity){
    //set line
    x1 = xA;
    y1 = yA;
    
    int iX = PApplet.parseInt(random(intensity));
    int iY = intensity - iX;
    x2 = constrain(xA + iX, 0, width);
    y2 = constrain(yA + iY, 0 , height);
    //x2 = xA + intensity;
    //y2 = xA + intensity;
  
    //pick random colour
    //r = int(random(255));
    //g = int(random(255));
    //b = int(random(255));
   
   //use colors from Nathan's design
   r = 240;
   g = 240;
   b = 239;  
  }
  
  public void update(){
    stroke(r,g,b);
    strokeWeight(2);
    line(x1,y1,x2,y2);
    
  }
  public void addSmile(){
      //SmileLine[] newSmile = append(smiles,SmileLine(400,200));
      //SmileLine smile = (SmileLine) smiles.get(smiles.size());
      smiles.add(new SmileLine(x2,y2,PApplet.parseInt(random(255))));
  }
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
    String[] appletArgs = new String[] { "smile" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
