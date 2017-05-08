//
//
//float soundX;
//float featureData[][] = new float[2][4];
//color detectionColor = color(255);
//
//
//void setup() {
//  size(640, 480);
//  for (int i=0; i<2; i++)
//    for (int j=0; j<4; j++)
//      featureData[i][j] = 0;
//}
//
//void draw() {
//  background(255);
//  soundX = readFile();
//  strokeWeight(100);
//  stroke(255, 0, 0);
//  point(soundX, height/2);
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
//  if (!Double.isNaN(xCoord))
//    println("xcord ", xCoord);
//  if ( xCoord > 1 ) xCoord = 1;
//  else if (xCoord < -1) xCoord = -1;
//  xCoord = map(xCoord, -1, 1, 0, width);
//  return xCoord;
//}

