//int width = ;
//int height = 1080;

//SmileLine l1 = new SmileLine(100,200);


//SmileLine[] smiles = new SmileLine[];
ArrayList smiles;

void setup(){

 size(1280, 720);
 background(0);
 frameRate(10);
 smiles = new ArrayList();
 
 //l1.init(100,200);
 smiles.add(new SmileLine(100,200,100));
}

void draw(){
  background(0);
  fill(0, 102, 153);
  smooth();

  text("Qualia-Smile", 15, 60); 

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
  
  
}

void keyPressed() {
    SmileLine smile = (SmileLine) smiles.get(smiles.size()-1);
    smile.addSmile();
}

class SmileLine {
  int x1,y1,z1,x2,y2,z2,angle,r,g,b;
  SmileLine(int xA,int yA,int intensity){
    //set line
    x1 = xA;
    y1 = yA;
    x2 = xA + intensity;
    y2 = xA + intensity;
  
    //pick random colour
    r = int(random(255));
    g = int(random(255));
    b = int(random(255)); 
  }
  
  void update(){
    stroke(r,g,b);
    strokeWeight(4);
    line(x1,y1,x2,y2);
    
  }
  void addSmile(){
      //SmileLine[] newSmile = append(smiles,SmileLine(400,200));
      //SmileLine smile = (SmileLine) smiles.get(smiles.size());
      smiles.add(new SmileLine(x2,y2,int(random(255))));
  }
}


