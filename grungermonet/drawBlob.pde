PVector positionA = new PVector(0, 0);
PVector positionB = new PVector(0, 0);

int timeDelay = 1;
int curTime;

void drawBlobsAndEdges() {
  noFill();
  Blob b;
  color pal[][] = new color[3][3];
  //color c[];
  EdgeVertex eA, eB;
  System s;
  float size = 0;
  int diffVal[] = new int[3];
  int sorting [] = new int[3];
  for (int i=0; i<3; i++) {
    diffVal[i] = -1;
    sorting[i] = -1;
    for (int j=0; j<3; j++)
      pal[i][j] = color(0);
  }
  userCount = 0;
  translate(0, (height-kinectHeight*reScale)/2);
  scale(reScale);
  //println("----------------", isVoice, "-------------------");
  if (isVoice) {
    //println(isVoice--, ": " );
    fill(255, 0, 0);
    //ellipse(soundX/3, kinectHeight/2, 30, 30);
    for (int n = 0; n < theBlobDetection.getBlobNb (); n++) {
      b = theBlobDetection.getBlob(n);
      count = 0;

      if (b != null) {
        // println( b.getEdgeNb ());
        if (b.getEdgeNb() > 200 && userCount < userSystem.size()) {
          s = userSystem.get(userCount);
          int t = second() - curTime;
          if (t < 0) t+= 60;
          t = timeDelay - t;
          if (b.getEdgeNb() > 400 && t < 0 ) {
            //println(t, "second flow ~!!!!");
            //    runParticle = !runParticle;
            curTime = second();
          }
          //else runParticle = false;

          for (int m = 0; m < b.getEdgeNb (); m+=1) {
            eA = b.getEdgeVertexA(m);
            eB = b.getEdgeVertexB(m);
            if ( eA != null && eB != null) {
              x = eA.x * width;
              y = eA.y * height;
              xB = eB.x * width;
              yB = eB.y * height;
              switch(state) {
              case 0:  
                {
                  if (m%2 == 0) {
                    frameRate(60);
                    position.set(x, y, 0);
                    s.addParticlePosition(position);
                    sum.add(position);
                    count++;
                  }
                  break;
                }
              case 1:  
                {
                  frameRate(15);
                  positionA.set(x, y, 0);
                  positionB.set(xB, yB, 0);
                  s.addEnergyPosition(positionA, positionB);
                  sum.add(positionA);
                  count++;
                  break;
                }
              case 2:  
                {
                  frameRate(60);
                  position.set(x, y, 0);
                  s.addFacePosition(position);
                  sum.add(position);
                  count++;
                }
                //stroke(0, 30);
                //line(x, y, xB, yB);
                //println("print", x, y);
                //  s.add(position);
                //strokeWeight(1);
              }
            }
          }
          //println(userCount, sum); 
          sum.div(count);
          s.addcenter(sum); /////////////////////
          //float alp =
          fill(255, 0, 0);
          size =abs( 1 - ( abs(sum.x - soundX/3) / (float)width));
          //int idx = setColorFunc(sum.x, (int)size*255);
          //          while ( palette[idx] == color (0)) {
          //            idx++;
          //            idx %= 7;
          //          }
          
          color c[] = setColorFunc(sum.x);
          //          if (runParticle) {
          //            for (int i=0; i<3; i++)  
          //              c[i] = color(red(paletteOrigin[i][(idx)%7]), green(paletteOrigin[i][(idx)%7]), blue(paletteOrigin[i][(idx)%7]));
          //            //            c[0] = color(red(paletteOrigin[0][(idx%4 +userCount*2)%7]), green(paletteOrigin[0][(idx%4 +userCount*2)%7]), blue(paletteOrigin[0][(idx%4 +userCount*2)%7])); 
          //            //            c[1] = color(red(paletteOrigin[1][(idx%4 +userCount*2)%7]), green(paletteOrigin[1][(idx%4 +userCount*2)%7]), blue(paletteOrigin[1][(idx%4 +userCount*2)%7])); 
          //            //            c[2] = color(red(paletteOrigin[2][(idx%4 +userCount*2)%7]), green(paletteOrigin[2][(idx%4 +userCount*2)%7]), blue(paletteOrigin[2][(idx%4 +userCount*2)%7]));
          //            //setColorFunc(sum.x, (int)size *255);
          //          } else {
          //            for (int i=0; i<3; i++)  
          //              c[i] = color(red(paletteOrigin[i][(idx)%7]), green(paletteOrigin[i][(idx)%7]), blue(paletteOrigin[i][(idx)%7]));
          //            //            c[0] = color(red(linePalette[0][(idx%4 + userCount*2 ) %7]), green(linePalette[0][(idx%4 + userCount*2 ) %7]), blue(linePalette[0][(idx%4 +userCount*2 ) %7]), (int)(size*255));
          //            //            c[1] = color(red(linePalette[1][(idx%4 + userCount*2 ) %7]), green(linePalette[1][(idx%4 + userCount*2 ) %7]), blue(linePalette[1][(idx%4 +userCount*2 ) %7]), (int)(size*255));
          //            //            c[2] = color(red(paletteOrigin[2][(idx%4 +userCount*2 ) %7]), green(paletteOrigin[2][(idx%4 +userCount*2 ) %7]), blue(paletteOrigin[2][(idx%4 +userCount*2 ) %7]), (int)(size*255));
          //          }
          // palette[idx] = color(0);
          //          s.setSize(volume*4);
          try {
            diffVal[userCount] = (int)abs(sum.x-soundX/3);
            pal[userCount++] = c;
          }
          catch (ArrayIndexOutOfBoundsException e) {
            println("??");
          }
          //          s.setColor(c);
          //          s.run();
          //userCount++;
        }
      }
      //}
      for (int i=0; i<3; i++) {
        if (diffVal[i] == -1) break;
        sorting[i] = 0;
        for (int j=0; j<3; j++) {
          if (i==j) continue;
          if (diffVal[j] == -1) break;
          if (diffVal[i] > diffVal[j])  sorting[i]++;
        }
      }
      //println("????");
      userCount=0;
      int min = 3;
      for (int i=0; i<3; i++) {
        if (diffVal[i] == -1)  break;
        if (sorting[i] < min) {
          min = sorting[i];
        }
        s = userSystem.get(i);
        s.setColor(pal[sorting[i]]);
        s.setSize(volume);
        s.setDir(sorting[i]);
        s.run();
        userCount++;
      }
    }
    for (int i=0; i<7; i++)
      palette[i] = paletteOrigin[0][i];
  }

  while (userCount < 3) {
    drawDefault(userCount);
    userCount++;
  }
}

void drawDefault(int i) {
  System s;
  for (i=0; i<userSystem.size (); i++) {
    s = userSystem.get(i);
    setDefault(s);
  }
}
void drawDefault(System s) {
  setDefault(s);
}
void setDefault(System s) {
  if (s.isEmpty()) {
    for (int i=0; i<200; i++) {
      position.set(random(width), random(height));
      s.addParticlePosition(position);
    }
  }
  //s.setColor(color(0, s.center.x/3, s.center.y/3)); 
  s.runDefault();
}

