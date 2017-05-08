void drawBlobsAndEdges() {
  noFill();
  Blob b;
  color c;
  EdgeVertex eA, eB;
  System s;
  userCount = 0;
  translate(0, (height-kinectHeight*reScale)/2);
  scale(reScale);
  for (int n = 0; n < theBlobDetection.getBlobNb (); n++) {
    b = theBlobDetection.getBlob(n);

    count = 0;
    if (b != null) {
      println(b.getEdgeNb());
      if (b.getEdgeNb() > 100 && userCount < userSystem.size()) {
        s = userSystem.get(userCount);
        for (int m = 0; m < b.getEdgeNb (); m+=2) {

          eA = b.getEdgeVertexA(m);
          eB = b.getEdgeVertexB(m);
          if ( eA != null && eB != null) {
            x = eA.x * width;
            y = eA.y * height;
            position.set(x, y, 0);
            s.add(position);
            sum.add(position);
            count++;
            //strokeWeight(1);
          }
        }
        println(userCount, sum); 
        sum.div(count);
        s.addcenter(sum); /////////////////////
        c = color(0, 255, 255);
        s.setColor(c);
        s.run();
        userCount++;
      }
    }
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

void setDefault(System s) {
  if (s.isEmpty()) {
    for (int i=0; i<200; i++) {
      position.set(random(width), random(height));
      s.add(position);
    }
  }
  //s.setColor(color(0, s.center.x/3, s.center.y/3)); 
  s.runDefault();
}

