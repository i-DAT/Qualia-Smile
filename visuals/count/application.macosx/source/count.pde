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


void setup(){

 size(width, height);
 background(0);
 frameRate(frames);
 
 font = loadFont("HelveticaNeue-Light-72.vlw");
 

 
 m = new MQTTLib(MQTT_BROKER, new MessageHandler());
 m.connect(CLIENT_ID, CLEAN_START, KEEP_ALIVE);
 m.subscribe(TOPICS, QOS);

 
}

void draw(){

  background(39,39,38);
  //stroke(210, 123, 34);
  textFont(font, 72);
  textAlign(CENTER);
  text(str(count), ((width/2)), (height/2));
        
  }

void keyPressed() {

    createSmile();
}



void createSmile(){
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


