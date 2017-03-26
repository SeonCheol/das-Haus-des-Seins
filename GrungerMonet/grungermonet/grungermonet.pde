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
// declare custom PolygonBlob object (see class for more info)f
PolygonBlob poly = new PolygonBlob();

// PImage to hold incoming imagery and smaller one for blob detection
PImage cam, blobs;
// the kinect's dimensions to be used later on for calculations
int kinectWidth = 640;
int kinectHeight = 480;
// to center and rescale from 640x480 to higher custom resolutions
float reScale;
float r = 0;
// background color
color bgColor;
// three color palettes (artifact from me storing many interesting color palettes as strings in an external data file ;-)
String[][] palettes = {
  {
    "-1117720,-13683658,-8410437,-9998215,-1849945,-5517090,-4250587,-14178341,-5804972,-3498634", 
    "-67879,-9633503,-8858441,-144382,-4996094,-16604779,-588031", 
    "-16711663,-13888933,-9029017,-5213092,-178706 3,-11375744,-2167516,-15713402,-5389468,-2064585"
  }
  , {
    "-1117720,-13683658,-8410437,-9998215,-1849945,-5517090,-4250587,-14178341,-5804972,-3498634", 
    "-16711663,-13888933,-9029017,-5213092,-178706 3,-11375744,-2167516,-15713402,-5389468,-2064585", 
    "-67879,-9633503,-8858441,-144382,-4996094,-16604779,-588031"
  }
};



int particleLength = 1300;
// an array called flow of 2250 Particle objects (see Particle class)
Particle[] flow = new Particle[particleLength];
// global variables to influence the movement of all particles
float globalX, globalY;

BufferedReader reader;

String line;
String [] c;

float featureData [][] = new float [2][4];
float size =8;
float sum_size = 0;
int idx = 1;
void setup() {

  // it's possible to customize this, for example 1920x1080
  size(640, 480);

  // initialize SimpleOpenNI object
  context = new SimpleOpenNI(this);
  if (!context.isInit()) {
    // if context.enableScene() returns false
    // then the Kinect is not working correctly
    // make sure the green light is blinking
    println("Kinect not connected!");
    exit();
  } else {
    // mirror the image to be more intuitive
    context.enableDepth();
    context.enableUser();
    context.setMirror(true);

    // calculate the reScale value
    // currently it's rescaled to fill the complete width (cuts of top-bottom)
    // it's also possible to fill the complete height (leaves empty sides)
    reScale = (float) width / kinectWidth; // reScale == 1

    // create a smaller blob image for speed and efficiency
    blobs = createImage(width, height, RGB);


    // initialize blob detection object to the blob image dimensions
    theBlobDetection = new BlobDetection(blobs.width, blobs.height);
    theBlobDetection.setThreshold(0.2); // block strength
    setupFlowfield();
  }
}


void draw() {
  background(0);
  cam = createImage(width, height, RGB);
  // update the SimpleOpenNI object
  context.update();
  // put the image into a PImage

    int[]depthValues= context.depthMap();
  int[] userMap = null;
  int userCount = context.getNumberOfUsers();
  System.gc();
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
    // clear the polygon (original functionality)
    poly.reset();
    // create the polygon from the blobs (custom functionality, see class)
    poly.createPolygon();
    drawFlowfield();
  }
  thread("readFile");
}


void readFile() {

  BufferedReader reader;
  String line;
  String splitData [];
  //  float size = 8;
  //  float sum_size = 0;
  //  int idx = 1;

  try {
    reader = createReader("data/dataForSound.data");
    line = reader.readLine();
    if (line == null) {
    } else {
      splitData = split(line, " ");

      for (int i=0; i<8; i++) {
        try {
          featureData[i/4][i%4] = float(splitData[i]);
          print(featureData[i/4][i%4]+ " ");
        }  
        catch (Exception e) {
          continue;
        }
        if (Double.isNaN(featureData[i/4][i%4])) {
          println("nan");
          break;
        }
      }
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
  println("===============================");
}

