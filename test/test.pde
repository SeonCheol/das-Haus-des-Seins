import ddf.minim.*;

AudioPlayer player;
Minim minim;

void setup(){
  size(1024, 200, P2D);

  minim = new Minim(this);
  player = minim.loadFile("Game of Thrones.mp3", 2048);
  player.play();
  player.loop();
}

void draw(){
  background(0);
  stroke(255);
  line(0,100,width,100);
  int count = 0;
  int lowTot = 0;
  int medTot = 0;
  int hiiTot = 0;
  for (int i = 0; i < player.left.size()/3.0; i+=5){
    lowTot+= (abs(player.left.get(i)) * 50 );
    count++;
  }
  fill( map( lowTot, 0, count * 50, 0, 255 ), 0, 0);
  noStroke();
  rect(0,0,20,20);
  stroke(255);
  
  
  for (int i = 0; i < player.left.size()-1; i+=5)
  {
//    line(i, 50 + player.left.get(i)*50, i+1, 50 + player.left.get(i+1)*50);
  //  line(i, 150 + player.right.get(i)*50, i+1, 150 + player.right.get(i+1)*50);
    point( 2*i, 100 + player.left.get(i)*50 );
    
  }
}

void stop(){
  player.close();
  minim.stop(); 
  super.stop();
}
