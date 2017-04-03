//
//// import libraries
//import SimpleOpenNI.*; // kinect
//import blobDetection.*; // blobs

// this is a regular java import so we can use and extend the polygon class (see PolygonBlob)
import java.awt.Polygon;
import java.util.Collections;

int widthSize = 640;
int heightSize = 480;
float x;
float featureData[][] = new float[2][4];
color detectionColor = color(255);

void setup() {
  size(widthSize, heightSize);
  x = width/2;
  fill(255);
  for (int i=0; i<2; i++)  
    for (int j=0; j<4; j++)
      featureData[i][j] = 0;
}

void draw() {
  background(0, 30);
  ellipse(x, height/2, 40, 40);
  x = readFile();
  print("location : ", x);
  x = map(x, -1, 1, 0, width);
  println(" " + x);

  fill(detectionColor);

  if (x > width/2 ) 
    detectionColor = setColor(x, 0);
  else 
    detectionColor = setColor(x, width);
  println();
  println();
}


color setColor(float x1, float x2) {
  float herz1, herz2;

  if (x > width/2) {
    herz1 = featureData[0][1];
    herz2 = featureData[1][1];
  } else {
    herz1 = featureData[1][1];
    herz2 = featureData[0][1];
  }
  print(herz1, herz2);
  color[] palette = {
    color(204, 142, 193), color(47, 45, 92), color(76, 129, 255), color(42, 144, 54), 
    color(253, 255, 84), color(255, 126, 50), color(256, 41, 0)
  };
  int lowBound = 50;
  int highBound = 330;
  int idx1 = int(herz1 - lowBound);
  int idx2 = int(herz2 - lowBound); 
  idx1 = int(herz1 / ((highBound - lowBound)/7));
  idx2 = int(herz2 / ((highBound - lowBound)/7));
  int r, g, b;
  int r1, g1, b1;
  int r2, g2, b2;
  float ratio;
  r = g = b = r1 = g1 = b1 = r2 = g2 = b2 = 0;

  if ( x1 > x2)  
    ratio = (x1 - x2) / x1;
  else
    ratio = (x2 - x1) / (width - x1);
  print("idx1 : ", idx1, "  idx2 : ", idx2);

  try {
    r1 =int( map(herz1, width/6 *idx1, width/6*(idx1+1), red(palette[idx1]), red(palette[idx1+1])));
    g1 =int( map(herz1, width/6 *idx1, width/6*(idx1+1), green(palette[idx1]), green(palette[idx1+1])));
    b1 =int( map(herz1, width/6 *idx1, width/6*(idx1+1), blue(palette[idx1]), blue(palette[idx1+1])));
  } 
  catch(Exception e) {
    if (idx1 >= 6) {
      r1 = 256;
      g1 = 41;
      b1 =0;
    }
  }
  try {
    r1 =int( map(herz2, width/6 *idx2, width/6*(idx2+1), red(palette[idx2]), red(palette[idx2+1])));
    g1 =int( map(herz2, width/6 *idx2, width/6*(idx2+1), green(palette[idx2]), green(palette[idx2+1])));
    b1 =int( map(herz2, width/6 *idx2, width/6*(idx2+1), blue(palette[idx2]), blue(palette[idx2+1])));
  } 
  catch(Exception e) {
    if (idx2 >= 6) {
      r2 = 256;
      g2 = 41;
      b2 =0;
    }
  }

  r =int( map(ratio, 0, 1, r1, r2));
  g =int( map(ratio, 0, 1, g1, g2));
  b =int( map(ratio, 0, 1, b1, b2));
  println(ratio, r1, g1, b1, r2, g2, b2, r, g, b);


  return color(r, g, b);
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
  return xCoord;
}

