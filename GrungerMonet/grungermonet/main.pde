

void setupFlowfield() {
  //// set stroke weight (for particle display) to 2.5
  strokeWeight(1);
  //// initialize all particles in the flow
  for (int i=0; i< flow.length; i ++) {
    flow[i] = new Particle(i/10000.0);
  }
  //// set all colors randomly now
  //  setRandomColors(1);
}


color setColor(float herz) {
  color[] palette = {
    color(204, 142, 193), color(47, 45, 92), color(76, 129, 255), color(42, 144, 54), 
    color(253, 255, 84), color(255, 126, 50), color(256, 41, 0)
  };
  int lowBound = 50;
  int highBound = 330;
  int idx = int(herz - lowBound);
  idx = int(herz / ((highBound - lowBound)/7));


  int r =int( map(herz, lowBound, width/6*(idx+1), red(palette[idx]), red(palette[idx+1])));
  int g =int( map(herz, width/6 *idx, width/6*(idx+1), green(palette[idx]), green(palette[idx+1])));
  int b =int( map(herz, width/6 *idx, width/6*(idx+1), blue(palette[idx]), blue(palette[idx+1])));

  return color(r, g, b);
}

void drawFlowfield() {
  for (int i=0; i < particleLength; i ++) {

    flow[i].col = setColor(featureData[0][1]);//colorPalette[int(random(1, colorPalette.length))];
  }
  //// center and reScale from Kinect to custom dimensions
  translate(0, (height-kinectHeight*reScale)/2);
  scale(reScale);
  //// set global variables that influence the particle flow's movement
  globalX = noise(frameCount * 0.01) * width/2 + width/4;
  globalY = noise(frameCount * 0.005 + 5) * height;
  //// update and display all particles in the flow
  for (Particle p : flow) {
    p.updateAndDisplay();
  }
}
//// sets the colors every nth frame
void setRandomColors(int nthFrame) {
  if (frameCount % nthFrame == 0) {
    // turn a palette into a series of strings
    String[] paletteStrings = split(palettes[0][int(random(palettes.length))], ',');
    // turn strings into colors
    color[] colorPalette = new color[paletteStrings.length];
    for (int i=0; i < paletteStrings.length; i ++) {
      colorPalette[i] = int(paletteStrings[i]);
    }

    // set all particle colors randomly to color from palette (excluding first aka background color)
    for (int i=0; i < particleLength; i ++) {

      println(r, g);
      flow[i].col = color(r, 0, 0);
    }
  }
}

void onNewUser(int userId) {
  println("detected" + userId);
}
void onLostUser(int userId) {
  println("lost: " + userId);
}
void keyPressed() {
  //  if (keyCode == UP)
  //    r += 10;
  //  else if (keyCode == DOWN)
  //    r -= 10;
  //
  //  println(r);
}

