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

// PImage to hold incoming imagery and smaller one for blob detection
PImage cam, blobs;
// the kinect's dimensions to be used later on for calculations
int kinectWidth = 640;
int kinectHeight = 480;
// to center and rescale from 640x480 to higher custom resolutions
float reScale;
float x, y;
float xB, yB;
// background color
color bgColor;
// global variables to influence the movement of all particles
float globalX, globalY;
PVector sum = new PVector(0, 0);
float count;
//ParticleSystem ps;
HashMap<Integer, System> userSystem;
int userCount;
PVector position = new PVector(0, 0);

System defaultSystem;

void setup() {
  // it's possible to customize this, for example 1920x1080
  //size(640, 480, P2D);
  size(1920, 1080, OPENGL);
  userSystem = new HashMap<Integer, System>();
  for (int i=0; i<3; i++) {
    System s = new System();
    userSystem.put(i, s);
  }

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
    reScale = (float) width / kinectWidth;
    // create a smaller blob image for speed and efficiency
    blobs = createImage(kinectWidth/2, kinectHeight/2, RGB);

    // initialize blob detection object to the blob image dimensions
    theBlobDetection = new BlobDetection(blobs.width, blobs.height);
    //user start
    theBlobDetection.setPosDiscrimination(true);
    //user end
    theBlobDetection.setThreshold(0.1);
    isVoice = false;
    //isVoice = 0;
  }


  curTime = second();

  defaultSystem = new System();
}

void draw() {
  //background(255);
  fill(255, 50);
  rect(0, 0, width, height);
  cam = createImage(width, height, RGB);
  // update the SimpleOpenNI object
  context.update();
  // put the image into a PImage

    int[] depthValues= context.depthMap();
  int[] userMap = null;
  int userCount = context.getNumberOfUsers();
  //if (userCount > 0) {
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
  drawBlobsAndEdges();
  soundX = readFile();
  //}
  fill(255, 0, 0);  
  //println("sound ::: ", soundX, width, kinectWidth, kinectHeight, mouseX, "-----------------------------------");
  //ellipse(soundX/2, kinectHeight/2, 50, 50);

  drawDefault(defaultSystem);
}

void onNewUser(int userId) {
  println("detected" + userId);
}
void onLostUser(int userId) {
  println("lost: " + userId);
}

void onVisibleUser(SimpleOpenNI curContext, int userId) {
  // println("onVisibleUser - userId: " + userId);
  //  if (userId > userSystem.size()) {
  //    System s = new System();
  //    userSystem.put(userId, s);
  //  }
}

