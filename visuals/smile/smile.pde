//int width = ;
//int height = 1080;

//SmileLine l1 = new SmileLine(100,200);


//SmileLine[] smiles = new SmileLine[];
ArrayList smiles;
ArrayList triangles;

int width = 1280;
int height = 720;
float theScale = 1;

void setup(){

 size(width, height);
 background(0);
 frameRate(12);
 
 smiles = new ArrayList();
 
 //l1.init(100,200);
 smiles.add(new SmileLine(100,200,100));
 
 
 triangles = new ArrayList();
 //triangles.add(new SmileTriangle(100,100));
 triangles.add(new SmileTriangle());
 
 
}

void draw(){
  scale(theScale);
  background(39,39,38);
  smooth();

  //text("Qualia-Smile", 15, 60); 

  //l1.update();
  //l1.addSmile();
  
  //loop through and display
  for(int i = 1; i <= smiles.size(); i++){
    //print(i);
    SmileLine smile = (SmileLine) smiles.get(i - 1);
    smile.update();
    //if (i == smiles.size()){
        //smile.addSmile();
    //}
    
    
  }
  
  for(int i = 1; i <= triangles.size(); i++){
    SmileTriangle smile = (SmileTriangle) triangles.get(i - 1);
    smile.update();    
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

void keyPressed() {
    SmileLine smile = (SmileLine) smiles.get(smiles.size()-1);
    smile.addSmile();
    
    SmileTriangle tri = (SmileTriangle) triangles.get(triangles.size()-1);
    tri.addAlignedTriangle();
    
    //theScale = theScale - 0.01;
}

class SmileTriangle {
    PVector pointA, pointB, pointC;
    int r,g,b;
    SmileTriangle(){
        pointA = new PVector(100,100);
        pointB = new PVector(200,200);
        pointC = new PVector(0,200);
        
         //use colors from Nathan's design
       r = 240;
       g = 240;
       b = 239; 
      
    }
    SmileTriangle(int x, int y){
        pointA = new PVector(x,y);
        pointB = new PVector(x+100,y+100);
        pointC = new PVector(x+int(random(100)),y+int(random(100)));
        
        //use colors from Nathan's design
       r = 240;
       g = 240;
       b = 239;  
    }
    SmileTriangle(int aX, int aY, int bX, int bY){
        pointA = new PVector(aX,aY);
        pointB = new PVector(bX,bY);
        pointC = new PVector(bX+int(random(100)),int(bY+random(100)));
        
        //use colors from Nathan's design
       r = 240;
       g = 240;
       b = 239;  
    }
    void update(){
        stroke(r,g,b);
        strokeWeight(2);
        //line(x1,y1,x2,y2); 
        triangle(pointA.x,pointA.y,pointB.x,pointB.y,pointC.x,pointC.y);
    }
    void addTriangle(){
      triangles.add(new SmileTriangle(int(pointC.x),int(pointC.y)));
    }
    void addAlignedTriangle(){
      triangles.add(new SmileTriangle(int(pointB.x),int(pointB.y),int(pointC.x),int(pointC.y)));
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
    
    int iX = int(random(intensity));
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
  
  void update(){
    stroke(r,g,b);
    strokeWeight(2);
    line(x1,y1,x2,y2);
    
  }
  void addSmile(){
      //SmileLine[] newSmile = append(smiles,SmileLine(400,200));
      //SmileLine smile = (SmileLine) smiles.get(smiles.size());
      smiles.add(new SmileLine(x2,y2,int(random(255))));
  }
}


