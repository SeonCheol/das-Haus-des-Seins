// true -> particle
// false -> line 
boolean runParticle = true;
int state = 0;
void changeMode() {
  runParticle = !runParticle;
  state = (state + 1) % 3;
}

void mouseClicked() {
  //runParticle = !runParticle;
  state = (state + 1) % 3;
}

class System {
  ArrayList<Particle> system;
  ArrayList<Energy> energySystem;
  ArrayList<Face> faceSystem;
  PVector center;
  color c[];
  int dir;

  System() {
    system = new ArrayList<Particle>();
    energySystem = new ArrayList<Energy>();
    faceSystem = new ArrayList<Face>();
    center = new PVector(200, 200);
    c = new color[3];
    dir = 0;
  }
  void addParticlePosition(PVector position) {
    Particle ps = new Particle(position);
    system.add(ps);
  }
  void addEnergyPosition(PVector positionA, PVector positionB) {
    Energy eg = new Energy(positionA, positionB);
    energySystem.add(eg);
  }

  void addFacePosition(PVector positionA) {
    Face fc = new Face(positionA);
    faceSystem.add(fc);
  }

  void setColor(color c[]) {
    this.c = c;
  }
  ////////////////////////////
  void addcenter(PVector s) {
    center = new PVector(s.x, s.y);
  }
  void setDir(int dir) {
    this.dir = dir;
  }
  void run() {
    switch(state) {
    case 0 : 
      runParticle();
      break;
    case 1: 
      runEnergy();
      break;
    case 2:
      runFace();
      break;
    }
    //    if (!runParticle)  
    //      runEnergy();
    //    else 
    //      //runParticle();
    //    runFace();
  }

  void runFace() {
    beginShape();
    noStroke();
    fill(c[0]);    
    for (int i=faceSystem.size ()-1; i>=0; i--) {
      println("i : ", i);
      Face fc = faceSystem.get(i);
      fc.run();
      if (fc.isDead()) {
        faceSystem.remove(i);
      }
    } 
    endShape(CLOSE);
  }

  void runParticle() {
    if (this.dir == 0) {
      for (int i = system.size ()-1; i >= 0; i--) {
        //if (i % (this.dir+1) == 0) {

        Particle ps = system.get(i);
        ps.setColor(c[i%4%c.length]);
        //ps.addParticle();
        ps.addcenter(center);///////////////////////////////

        ps.run();
        if (i % 5 == 0) { 
          Particle tmpPs = new Particle(new PVector(ps.x, ps.y));
          tmpPs.setColor(c[i%4%c.length]);
          tmpPs.run();
        } 
        if (ps.isDead()) {
          system.remove(i);
        }
      }
    } else
      for (int i = system.size ()-1; i >= 0; i--) {
      if (i % (10 - this.dir*2) == 0) {
        //system.remove(i);
        //continue;
      }
      Particle ps = system.get(i);
      ps.setColor(c[i%4%c.length]);
      //ps.addParticle();
      ps.addcenter(center);///////////////////////////////

      ps.runDefault();
      if (ps.isDead()) {
        system.remove(i);
      }
    }
  }
  void runEnergy() {
    for (int i = energySystem.size ()-1; i>=0; i--) {
      Energy eg = energySystem.get(i);
      eg.setColor(c);
      //ps.addParticle();
      eg.setDir(dir);
      eg.addcenter(center);
      eg.run();
      if (eg.isDead()) {
        energySystem.remove(i);
      }
    }
  }
  boolean isEmpty() {
    return system.isEmpty();
  }
  boolean energyIsEmpty() {
    return energySystem.isEmpty();
  }
  void runDefault() {
    for (int i = system.size ()-1; i >= 0; i--) {
      Particle ps = system.get(i);
      ps.setColor(c[i%c.length]);
      //ps.addParticle();
      ps.addcenter(new PVector(random(width), random(height)));///////////////////////////////
      ps.runDefault();
      if (ps.isDead()) {
        system.remove(i);
      }
    }
  }
  void setSize(float size) {
    for (int i = system.size ()-1; i >= 0; i--) {
      Particle ps = system.get(i);
      ps.setSize(size);
    }
  }
}




// A simple Particle class
class Particle {
  PVector center;
  float x, y;
  float lerpRand;
  color c;
  float lifespan;
  float xDir, yDir;
  float vel;
  float mag;
  float size;

  Particle(PVector l) {
    this.x = l.x;
    this.y = l.y;
    if ((int)random(2) == 0)  
      this.xDir =random(-2, 2);
    else
      this.yDir = random(-2, 2);
    this.lerpRand = random(0.01, 0.1);
    lifespan = 300.0;
    this.vel = random(15);
    this.mag = random(15);
    c = color(0, 255, 255);
    size = 1;
  }
  void run() {
    update();
    display();
  }
  void runDefault() {
    updateDefault();
    display();
  }
  // Method to update position
  void update() {
    //    x = lerp(x, center.x, lerpRand);
    //    y = lerp(y, center.y, lerpRand);
    lifespan -= 20.0;
  }
  void setColor(color c) {
    this.c = c;
  }
  ////////////////////
  void addcenter(PVector s) {
    center = new PVector(s.x, s.y);
  }
  // Method to display
  void display() {
    //stroke(0, lifespan);
    strokeWeight(0.2);
    fill(c, lifespan);
    stroke(c, lifespan);
    //    line(this.x, this.y, this.x+random(-5, 5), this.y +random(-5, 5));
    ellipse(this.x, this.y, size, size);
  }
  void updateDefault() {
    if (xDir != 0) {
      xDir += vel;
      y += mag * sin(yDir);
    } else yDir += vel;
    x += mag * sin(xDir);
    y += mag * sin(yDir);
    lifespan -= 10.0;
  }
  // Is the particle still useful?
  boolean isDead() {
    if (lifespan < 0.0) {
      return true;
    } else {
      return false;
    }
  }
  void setSize(float size) {
    this.size = size;
  }
}

// A Simple Energy class
class Energy {
  PVector center;
  float xA, yA;
  float xB, yB;
  float xA2, yA2;
  float xB2, yB2;
  float lerpRandA;
  float lerpRandB;
  color c;
  float lifespan;
  float xDir, yDir;
  float vel;
  float mag;
  int dir;

  color pal[];

  Energy(PVector A, PVector B) {
    this.xA = A.x;
    this.yA = A.y;
    this.xB = B.x;
    this.yB = B.y;
    this.lerpRandA = -0.00001;
    this.lerpRandB = 0.01;
    lifespan = 300.0;
    this.vel = random(15);
    this.mag = random(15);
    c = color(0); //color(0, 255, 255);
    pal = new color[3];
  }
  void run() {
    update();
    display();
  }
  void runDefault() {
    updateDefault();
    display();
  }
  // Method to update position
  void update() {
    xA = lerp(xA, center.x, lerpRandA);
    yA = lerp(yA, center.y, lerpRandA);
    xB = lerp(xB, center.x, lerpRandA);
    yB = lerp(yB, center.y, lerpRandA);
    lifespan -= 50.0; // 50

      c = lerpColor(this.pal[0], this.pal[1], map(lifespan, 300, 0, 0, 1.0));
  }
  void setColor(color c[]) {
    this.pal = c;
    //this.c = c;
  }
  ////////////////////
  void addcenter(PVector s) {
    center = new PVector(s.x, s.y);
  }
  // Method to display
  void display() {
    stroke(c);
    strokeWeight(volume / 2);
    //fill(255, lifespan);
    line(xA, yA, xB, yB);
  }
  void updateDefault() {
    //    if (xDir != 0) {
    //      xDir += vel;
    //      y += mag * sin(yDir);
    //    } else yDir += vel;
    //    x += mag * sin(xDir);
    //    y += mag * sin(yDir);
    //    lifespan -= 20.0;
  }
  // Is the particle still useful?
  boolean isDead() {
    if (lifespan < 0.0) {
      return true;
    } else {
      return false;
    }
  }

  void setDir(int dir) {
    //println("dir : ", dir);
    if (dir == 0) {
      this.lerpRandA = -.001;
    } else { 
      this.lerpRandA = .15;
    }
  }
}



class Face {
  PVector center;
  float xA, yA;
  float xA2, yA2;
  float xB2, yB2;
  float lerpRandA;
  float lerpRandB;
  color c;
  float lifespan;
  float xDir, yDir;
  float vel;
  float mag;
  int dir;

  color pal[];

  Face(PVector A) {
    this.xA = A.x;
    this.yA = A.y;
    this.lerpRandA = -0.00001;
    this.lerpRandB = 0.01;
    lifespan = 300.0;
    this.vel = random(15);
    this.mag = random(15);
    c = color(0); //color(0, 255, 255);
    pal = new color[3];
  }
  void run() {
    update();
    display();
  }
  void runDefault() {
    updateDefault();
    display();
  }
  // Method to update position
  void update() {
    //    xA = lerp(xA, center.x, lerpRandA);
    //    yA = lerp(yA, center.y, lerpRandA);
    //    xB = lerp(xB, center.x, lerpRandA);
    //    yB = lerp(yB, center.y, lerpRandA);
    lifespan -= 50.0; // 50
    c = lerpColor(this.pal[0], this.pal[1], map(lifespan, 300, 0, 0, 1.0));
  }
  void setColor(color c[]) {
    this.pal = c;
    //this.c = c;
  }
  ////////////////////
  void addcenter(PVector s) {
    center = new PVector(s.x, s.y);
  }
  // Method to display
  void display() {
    //stroke(c);
    //strokeWeight(volume / 2);
    //line(xA, yA, xB, yB);
    vertex(xA, yA);
  }
  void updateDefault() {
    //    if (xDir != 0) {
    //      xDir += vel;
    //      y += mag * sin(yDir);
    //    } else yDir += vel;
    //    x += mag * sin(xDir);
    //    y += mag * sin(yDir);
    //    lifespan -= 20.0;
  }
  // Is the particle still useful?
  boolean isDead() {
    if (lifespan < 0.0) {
      return true;
    } else {
      return false;
    }
  }

  void setDir(int dir) {
    //println("dir : ", dir);
    if (dir == 0) {
      this.lerpRandA = -.001;
    } else { 
      this.lerpRandA = .15;
    }
  }
}

