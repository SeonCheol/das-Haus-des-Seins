////// import libraries
////import SimpleOpenNI.*; // kinect
////import blobDetection.*; // blobs
//
//// this is a regular java import so we can use and extend the polygon class (see PolygonBlob)
//import java.awt.Polygon;
//import java.util.Collections;
//
//int widthSize = 640;
//int heightSize = 480;
//float x;
//float featureData[][] = new float[2][4];
//color detectionColor = color(255);
//
//void setup() {
//  size(widthSize, heightSize);
//  x = width/2;
//  fill(255);
//  for (int i=0; i<2; i++)  
//    for (int j=0; j<4; j++)
//      featureData[i][j] = 0;
//}
//
//void draw() {
//  background(0, 30);
//  ellipse(x, height/2, 40, 40);
//  x = readFile();
//  print("location : ", x);
//  x = map(x, -1, 1, 0, width);
//  println(" " + x);
//  fill(detectionColor);
//  if (x > width/2 )  detectionColor = setColor(x, 0);
//  else  detectionColor = setColor(x, width);
//  println();
//  println();
//}


//color setColor(float x1, float x2) {
//  float herz1, herz2;
//  float herz[2];
//
//  if (x > width/2) {
//    herz[0] = featureData[0][1];
//    herz[1] = featureData[1][1];
//  } else {
//    herz[0] = featureData[1][1];
//    herz[1] = featureData[0][1];
//  }
//  print(herz[0], herz[1]);
//
//  color[] palette = {
//    color(204, 142, 193), color(47, 45, 92), color(76, 129, 255), color(42, 144, 54), 
//    color(253, 255, 84), color(255, 126, 50), color(256, 41, 0)
//  };
//  int lowBound = 50;
//  int highBound = 330;
//  int idx[2];
//  int r[3], g[3], b[3];
//  float ration;
//
//  for (int i=0; i<2; i++) {
//    herz[i] -= lowBound;
//    idx[i] = int(herz[i] / ((highBound - lowBound) / 7 ) );
//    r[i] = g[i] = b[i] = 0;
//
//    try {
//      r[i] = int( map(herz[i], width/6 *idx[i], width/6*(idx[i]+1), red(palette[idx[i]]), red(palette[idx[i]+1])));
//      g[i] = int( map(herz[i], width/6 *idx[i], width/6*(idx[i]+1), red(palette[idx[i]]), red(palette[idx[i]+1])));
//      b[i] = int( map(herz[i], width/6 *idx[i], width/6*(idx[i]+1), red(palette[idx[i]]), red(palette[idx[i]+1])));
//    }
//    catch(Exception e) {
//      if (idx[i] >= 6) {
//        r[i] = 256;
//        g[i] = 41;
//        b[i] = 0;
//      }
//    }
//  }
//  if ( x1 > x2 )
//    ratio = (x1 - x2) / x1;
//  else
//    ratio = (x2 - x1) / (width - x1);
//
//  r[2] =int( map(ratio, 0, 1, r[0], r[1]));
//  g[2] =int( map(ratio, 0, 1, g[0], g[1]));
//  b[2] =int( map(ratio, 0, 1, b[0], b[1]));
//
//  println(ratio, r[0], g[0], b[0], r[1], g[1], b[1], r[2], g[2], b[2]);
//
//  return color(r[2], g[2], b[2]);
//}
//
//float readFile() {
//  BufferedReader reader;
//  String line;
//  String splitData [];
//  //  float size = 8;
//  //  float sum_size = 0;
//  //  int idx = 1;
//  boolean isVoice = false;
//  float xCoord = -1;
//
//  try {
//    reader = createReader("data/dataForSound.data");
//    line = reader.readLine();
//    if (line == null) {
//    } else {
//      splitData = split(line, " ");
//      for (int i=0; i<8; i++) {
//        try {
//          featureData[i/4][i%4] = float(splitData[i]);          
//          //  print(featureData[i/4][i%4]+ " ");
//        }
//        catch (Exception e) {
//          continue;
//        }
//        if (Double.isNaN(featureData[i/4][i%4])) {
//          break;
//        }
//        if (featureData[0][0] == float(-1))
//          isVoice = false;
//        else 
//          isVoice = true;
//      }
//      xCoord = float(splitData[splitData.length-1]);
//      // xCoord -> mapping!!
//      reader.close();
//    }
//  }
//  catch(IOException e) {
//    e.printStackTrace();
//    line = null;
//  }
//  catch(NullPointerException e) {
//    e.printStackTrace();
//  }
//  return xCoord;
//}
//
//
//
//
//
//
//
//
//
//

//BlobKinnect Created by Chloe 2014
// Inspired by Kinect Flow Example by Amnon Owed (15/09/12)

// import libraries
import SimpleOpenNI.*; // kinect
import blobDetection.*; // blobs

// this is a regular java import so we can use and extend the polygon class (see PolygonBlob)
import java.awt.Polygon;
import java.util.Collections;

// declare SimpleOpenNI object
SimpleOpenNI context;
// declare BlobDetection object
BlobDetection theBlobDetection;
// declare custom PolygonBlob object (see class for more info)
//PolygonBlob poly = new PolygonBlob();

// PImage to hold incoming imagery and smaller one for blob detection
PImage cam, blobs;
// the kinect's dimensions to be used later on for calculations
int kinectWidth = 640;
int kinectHeight = 480;
// to center and rescale from 640x480 to higher custom resolutions
float reScale;
float x, y;
// background color
color bgColor;
// three color palettes (artifact from me storing many interesting color palettes as strings in an external data file ;-)
//String[] palettes = {
//  "-1117720,-13683658,-8410437,-9998215,-1849945,-5517090,-4250587,-14178341,-5804972,-3498634", 
//  "-67879,-9633503,-8858441,-144382,-4996094,-16604779,-588031", 
//  "-16711663,-13888933,-9029017,-5213092,-1787063,-11375744,-2167516,-15713402,-5389468,-2064585"
//};

// an array called flow of 2250 Particle objects (see Particle class)
//Particle[] flow = new Particle[2250];
// global variables to influence the movement of all particles

float globalX, globalY;
PVector sum = new PVector(0, 0);
float count;
ParticleSystem ps;
System s;
PVector position = new PVector(0, 0);

/************
 Seoncheol
 ***********/
// location variable

float soundX;
float featureData[][] = new float[2][4];
color detectionColor = color(255);




void setup() {
  // it's possible to customize this, for example 1920x1080
  size(640, 480, P2D);
  s = new System();
  // initialize SimpleOpenNI object
  context = new SimpleOpenNI(this);
  if (!context.isInit()) {
    // if context.enableScene() returns false
    // then the Kinect is not working correctly
    // make sure the green light is blinking
    //  println("Kinect not connected!");
    exit();
  } else {
    // mirror the image to be more intuitive
    context.enableDepth();
    context.enableUser();
    context.setMirror(true);
    // calculate the reScale value
    // currently it's rescaled to fill the complete width (cuts of top-bottom)
    // it's also possible to fill the complete height (leaves empty sides)
    reScale = (float) width / kinectWidth;
    // create a smaller blob image for speed and efficiency
    blobs = createImage(width, height, RGB);

    // initialize blob detection object to the blob image dimensions
    theBlobDetection = new BlobDetection(blobs.width, blobs.height);
    //user start
    theBlobDetection.setPosDiscrimination(true);
    //user end
    theBlobDetection.setThreshold(0.2);
    //setupFlowfield();
    soundX= width/2;
    fill(255);
    for (int i=0; i<2; i++)
      for (int j=0; j<4; j++)
        featureData[i][j] = 0;
  }
}



void draw() {
  background(255);
  cam = createImage(width, height, RGB);
  // update the SimpleOpenNI object
  context.update();
  // put the image into a PImage

    int[] depthValues= context.depthMap();
  int[] userMap = null;
  int userCount = context.getNumberOfUsers();
  //if(frameCount % 100 == 0 ) print(userCount);
  if (userCount > 0) {
    userMap = context.userMap();
    cam.loadPixels();

    for (int y=0; y<context.depthHeight (); y++) {
      for (int x=0; x<context.depthWidth (); x++) {
        int index = x + y * context.depthWidth();
        if (userMap != null && userMap[index] > 0) {
          cam.set(x, y, 255); // put your sample random text
        }
      }
    }
    cam.updatePixels();

    //// copy the image into the smaller blob image
    blobs.copy(cam, 0, 0, cam.width, cam.height, 0, 0, blobs.width, blobs.height);
    // blur the blob image
    blobs.filter(BLUR);
    // detect the blobs
    theBlobDetection.computeBlobs(blobs.pixels);
    //user start
    drawBlobsAndEdges(true);
    //s.run();
    //user end
    // clear the polygon (original functionality)
    //poly.reset();
    // create the polygon from the blobs (custom functionality, see class)
    //poly.createPolygon();
    soundX = readFile();
  }
}


void onNewUser(int userId) {
  //println("detected" + userId);
}
void onLostUser(int userId) {
  println("lost: " + userId);
}
void drawBlobsAndEdges(boolean drawEdges) {
  noFill();
  Blob b;
  color c;
  EdgeVertex eA, eB;
  // print("???");

  for (int n = 0; n < theBlobDetection.getBlobNb (); n++) {
    b = theBlobDetection.getBlob(n);
    System s;
    sum.set(0, 0);
    count = 0;
    if (b != null) {
      if (drawEdges) {
        //stroke(255, 50);
        if (b.getEdgeNb() > 1000) {
          //println(b.getEdgeNb());
          s = new System();
          for (int m = 0; m < b.getEdgeNb (); m+=20) { // num of point is m
            // println(b.getEdgeNb());
            eA = b.getEdgeVertexA(m);
            eB = b.getEdgeVertexB(m);
            if ( eA != null && eB != null) {
              //strokeWeight(3);
              x = eA.x * width;// + random(-30, 30);
              y = eA.y * height;// + random(-30, 30);
              //if (m % 50 == 0) {
              position.set(x, y, 0);
              s.add(position);
              sum.add(position);
              count++;
              strokeWeight(1);
              //              line(eA.x * width, eA.y * height, x, y);
              //}
              //            strokeWeight(1);
              //            line(eA.x * width, eA.y * height, eB.x * width, eB.y * height);
            }
          }
          sum.div(count);
          //** seoncheol **//
          float alp = 1 - (abs(soundX - sum.x) / width);
          alp = int( map(alp, 0, 1, 0, 255) );
          if (!Double.isNaN(soundX))
            println(" ratio : ", alp, " sumX : ", sum.x, "  sound X : ", soundX, "  alp : ", alp, n);
          println();
          c = setColor(sum.x, (int)alp);

          s.setColor(c);
          if (s != null)
          {
            while (!s.isDead ())
              s.run();
          }
          strokeWeight(100);
          point(sum.x, sum.y);
          stroke(255, 0, 0);
          point(soundX, height/2);
        }
      }
    }
  }
}

class System {
  ArrayList<ParticleSystem> system;
  int lifeSpan = 50;
  color c;
  System() {
    system = new ArrayList<ParticleSystem>();
  }
  void add(PVector position) {
    ParticleSystem ps = new ParticleSystem(position);
    system.add(ps);
  }
  void setColor(color c) {
    this.c = c;
  }
  void run() {
    for (ParticleSystem ps : system) {
      ps.setColor(c);
      ps.addParticle();
    }
    lifeSpan -= 2; //
    for (int i = system.size ()-1; i >= 0; i--) {
      ParticleSystem ps = system.get(i);

      ps.run();
      if (ps.isDead()) {
        system.remove(i);
      }
    }

    //    sum.div(count);
    //    println(sum);
    //    stroke(255, 0, 0);
    //    strokeWeight(10);
    //    
    //    point(sum.x, sum.y);
  }
  boolean isDead() {//
    return (lifeSpan < 0.0);
  }
}
class ParticleSystem {
  ArrayList<Particle> particles;
  PVector origin;
  color c;
  int lifeSpan = 20;
  ParticleSystem(PVector position) {
    origin = new PVector(position.x, position.y);
    particles = new ArrayList<Particle>();
  }
  void setColor(color c)
  {
    this.c = c;
  }
  void addParticle() {
    particles.add(new Particle(origin, c));
  }

  void run() {
    lifeSpan -= 4;
    for (int i = particles.size ()-1; i >= 0; i--) {
      Particle p = particles.get(i);
      p.run();
      if (p.isDead()) {
        particles.remove(i);
      }
    }
  }
  boolean isDead() {
    return (lifeSpan < 0.0);
  }
}


// A simple Particle class

class Particle {
  PVector position;
  PVector velocity;
  PVector acceleration;
  color c;
  float lifespan;

  Particle(PVector l, color c) {
    acceleration = new PVector(0, 2);
    velocity = new PVector(random(-5, 5), random(-5, 5));
    position = new PVector(l.x, l.y, 0);
    this.c = c;
    lifespan = 255.0;
  }

  void run() {
    update();
    display();
  }

  // Method to update position
  void update() {
    velocity.add(acceleration);
    position.add(velocity);
    lifespan -= 25.0;
  }
  // Method to display
  void display() {
    stroke(c, lifespan);
    fill(c, lifespan);
    ellipse(position.x, position.y, 4, 4);
  }

  // Is the particle still useful?
  boolean isDead() {
    if (lifespan < 0.0) {
      return true;
    } else {
      return false;
    }
  }
}
void onVisibleUser(SimpleOpenNI curContext, int userId) {
  // println("onVisibleUser - userId: " + userId);
}
/** Seoncheol **/
/*
 *
 *
 *
 *
 **
 */
color setColor(float manX, int alp) {
  float herz[] = new float[2];
  if (x > width/2) {
    herz[0] = featureData[0][1];
    herz[1] = featureData[1][1];
  } else {
    herz[0] = featureData[1][1];
    herz[1] = featureData[0][1];
  }

  if (alp > 255)  alp = 255;
  else if (alp < 0) alp = 0;
  color[] palette = {
    color(204, 142, 193), color(47, 45, 92), color(76, 129, 255), color(42, 144, 54), 
    color(253, 255, 84), color(255, 126, 50), color(256, 41, 0)
  };
  int lowBound = 60;
  int highBound = 360;
  int idx[] = new int[2];
  int r[], g[], b[];
  float ratio;
  int len;

  r = new int[3];
  g = new int[3];
  b = new int[3];

  len = highBound - lowBound;
  len /= 6;
  for (int i=0; i<2; i++) {
    herz[i] -= lowBound;
    idx[i] = int(herz[i] / (len / 6) );
    r[i] = g[i] = b[i] = 0;
    try {
      r[i] = int( map(herz[i], len *idx[i], len*(idx[i]+1), red(palette[idx[i]]), red(palette[idx[i]+1])));
      g[i] = int( map(herz[i], len *idx[i], len*(idx[i]+1), green(palette[idx[i]]), green(palette[idx[i]+1])));
      b[i] = int( map(herz[i], len *idx[i], len*(idx[i]+1), blue(palette[idx[i]]), blue(palette[idx[i]+1])));
    }
    catch(Exception e) {
      if (idx[i] >= 6) {
        r[i] = 256;
        g[i] = 41;
        b[i] = 0;
      } else if (idx[i] <0 ) {
        r[i] = 204;
        g[i] = 142;
        b[i] = 193;
      }
    }
  }
  //  
  //  if ( x1 > x2 )
  //    ratio = (x1 - x2) / x1;
  //  else
  //    ratio = (x2 - x1) / (width - x1);
  //
  //  r[2] =int( map(ratio, 0, 1, r[0], r[1]));
  //  g[2] =int( map(ratio, 0, 1, g[0], g[1]));
  //  b[2] =int( map(ratio, 0, 1, b[0], b[1]));
  //
  println(r[2], g[2], b[2]);
  println();
  return color(r[2], g[2], b[2], alp);
}

float readFile() {
  BufferedReader reader;
  String line;
  String splitData [];
  //  float size = 8;
  //  float sum_size = 0;
  //  int idx = 1;
  boolean isVoice = false;
  float xCoord = -1;
  try {
    reader = createReader("data/dataForSound.data");
    line = reader.readLine();
    if (line == null) {
    } else {
      splitData = split(line, " ");
      for (int i=0; i<8; i++) {
        try {
          featureData[i/4][i%4] = float(splitData[i]);          
          //  print(featureData[i/4][i%4]+ " ");
        }
        catch (Exception e) {
          continue;
        }
        if (Double.isNaN(featureData[i/4][i%4])) {
          break;
        }
        if (featureData[0][0] == float(-1))
          isVoice = false;
        else 
          isVoice = true;
      }
      xCoord = float(splitData[splitData.length-1]);
      // xCoord -> mapping!!
      reader.close();
    }
  }
  catch(IOException e) {
    e.printStackTrace();
    line = null;
  }
  catch(NullPointerException e) {
    e.printStackTrace();
  }
  println("xcord ", xCoord);
  if ( xCoord > 1 ) xCoord = 1;
  else if (xCoord < -1) xCoord = -1;
  xCoord = map(xCoord, 0, 1, 0, width);
  return xCoord;
}

