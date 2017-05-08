float soundX;
float featureData[][] = new float[2][4];
color detectionColor = color(255);
boolean isVoice;
//int isVoice;


color[][] paletteOrigin = {
  {  
    color(115, 0, 70), color(27, 62, 89), color(60, 186, 200), color(133, 219, 24), 
    color( 255, 229, 0), color(255, 127, 0), color(185, 18, 27)
  }
  , 
  {  
    color(191, 187, 17), color(242, 240, 240), color(147, 237, 212), color(205, 232, 85), 
    color(155, 181, 143), color(255, 217, 51), color(76, 27, 27)
  }
  , 
  {  
    color(255, 194, 0), color(255, 172, 0), color(243, 245, 196), color(245, 246, 212), 
    color(255, 213, 150), color(204, 204, 82), color(246, 228, 151)
  }
};

color[][] linePalette = {
  {  
    color(115, 0, 70), color(27, 62, 89), color(60, 186, 200), color(133, 219, 24), 
    color( 255, 229, 0), color(255, 127, 0), color(185, 18, 27)
  }
  , 
  {  
    color(250, 5, 158), color(77, 220, 247), color(139, 233, 255), color(211, 250, 209), 
    color(155, 181, 143), color(255, 217, 51), color(255, 30, 30)
  }
};


color[] palette = {
  color(204, 142, 193), color(47, 45, 92), color(76, 129, 255), color(42, 144, 54), 
  color(253, 255, 84), color(255, 126, 50), color(256, 41, 0)
};





float readFile() {
  BufferedReader reader;
  String line;
  String splitData [];
  //  float size = 8;
  //  float sum_size = 0;
  //  int idx = 1;

  float xCoord = -1;
  try {
    reader = createReader("C:/Users/seoncheol/Documents/python/python_for_sound/GrungerMonet/grungermonet/data/dataForSound.data");
    line = reader.readLine();
    if (line == null) {
    } else {
      splitData = split(line, " ");
      int j=0;
      int i=1;
      featureData[0][0] = float(splitData[0]);
      j++;
      if (featureData[0][0] == float(-1))  
        i=4;
      for (; i<8; i++) {
        try {
          featureData[i/4][i%4] = float(splitData[j++]);
        }
        catch (Exception e) {
          continue;
        }
        if (Double.isNaN(featureData[i/4][i%4])) {
          break;
        }
        if (featureData[0][0] == float(-1)) {
          //isVoice = false;
          //isVoice = 0;
        } else 
          isVoice = true;
        //isVoice = 100;
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
  if ( xCoord > 1 ) xCoord = 1;
  else if (xCoord < -1) xCoord = -1;
  xCoord = map(xCoord, -1, 1, width, 0);
  //println("xcord : ", xCoord);
  fill(0);
  stroke(0);

  //
  return xCoord;
}



int setColorFunc(float manX, int alp) {
  float herz[] = new float[2];
  float ratio;
  color returnCol[] = new color[3];
  if (soundX > width/2) {
    herz[0] = featureData[0][1];
    herz[1] = featureData[1][1];
  } else {
    herz[0] = featureData[1][1];
    herz[1] = featureData[0][1];
  }
  if (alp > 255)  alp = 255;
  else if (alp < 0) alp = 0;
  //  color[] palette = {
  //    color(204, 142, 193), color(47, 45, 92), color(76, 129, 255), color(42, 144, 54), 
  //    color(253, 255, 84), color(255, 126, 50), color(256, 41, 0)
  //  };
  int lowBound = 60;
  int highBound = 360;
  int idx[] = new int[2];
  int r[], g[], b[];
  int len;
  int resultIdx= 0;

  r = new int[3];
  g = new int[3];
  b = new int[3];

  len = highBound - lowBound;
  len /= 6;

  ratio = abs(herz[0] - herz[1]);
  ratio /= width;

  for (int i=0; i<2; i++) {
    herz[i] -= lowBound;
    idx[i] = int(herz[i] / (len / 6));
  }

  resultIdx = (int)( idx[0] * ratio + idx[1] * (1-ratio) );
  if (resultIdx >= 6)      resultIdx = 6;
  else if (resultIdx < 0 ) resultIdx = 0;
  return resultIdx;
}
//
//  for (int i=0; i<2; i++) {
//    herz[i] -= lowBound;
//    idx[i] = int(herz[i] / (len / 6) );
//    r[i] = g[i] = b[i] = 0;
//    try {
//      r[i] = int( map(herz[i], len *idx[i], len*(idx[i]+1), red(palette[idx[i]]), red(palette[idx[i]+1])));
//      g[i] = int( map(herz[i], len *idx[i], len*(idx[i]+1), green(palette[idx[i]]), green(palette[idx[i]+1])));
//      b[i] = int( map(herz[i], len *idx[i], len*(idx[i]+1), blue(palette[idx[i]]), blue(palette[idx[i]+1])));
//    }
//    catch(Exception e) {
//      if (idx[i] >= 6) {
//        r[i] = 256;
//        g[i] = 41;
//        b[i] = 0;
//      } else if (idx[i] <0 ) {
//        r[i] = 204;
//        g[i] = 142;
//        b[i] = 193;
//      }
//    }
//  }
//  r[2] =int( map(ratio, 0, 2, r[0], r[1]));
//  g[2] =int( map(ratio, 0, 2, g[0], g[1]));
//  b[2] =int( map(ratio, 0, 2, b[0], b[1]));
//  //
//
//  returnCol[0] = color(r[2], g[2], b[2]);
//  returnCol[1] = palette[idx[0] % palette.length];
//  returnCol[2] = palette[idx[1] % palette.length];
//
//return returnCol;
//}

