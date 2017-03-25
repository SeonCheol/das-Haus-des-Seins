BufferedReader reader;

String line;
String [] c;

float featureData [][] = new float [2][4];
float size =8;
ParticleSystem ps;
float sum_size = 0;
int idx = 1;
void setup() {
  size(400, 400);
  // Starts a myServer on port 5204
  ps = new ParticleSystem(new PVector(width/2, 50));
  for (int i=0; i<2; i++) {
    for (int j=0; j<4; j++) {
      featureData[i][j] = 2;
    }
  }
}


float[] readFile() {

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
          featuresplitData.length - 1ata[i/4][i%4] = float(splitData[i]);
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

  return featureData;
}

