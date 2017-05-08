class System {
  ArrayList<Particle> system;
  PVector center;
  
  color c;
  System() {
    system = new ArrayList<Particle>();
    center = new PVector(200, 200);
  }
  void add(PVector position) {
    Particle ps = new Particle(position);
    system.add(ps);
  }
  void setColor(color c) {
    this.c = c;
  }
  ////////////////////////////
  void addcenter(PVector s) {
    center = new PVector(s.x, s.y);
  }
  void run() {
    for (Particle ps : system) {
      ps.setColor(c);
      //ps.addParticle();
      ps.addcenter(center);///////////////////////////////
    }

    for (int i = system.size ()-1; i >= 0; i--) {
      Particle ps = system.get(i);

      ps.run();
      if (ps.isDead()) {
        system.remove(i);
      }
    }
  }
  boolean isEmpty(){
    return system.isEmpty();
  }
  void runDefault() {
    for (Particle ps : system) {
      ps.setColor(c);
      //ps.addParticle();
      ps.addcenter(new PVector(random(width), random(height)));///////////////////////////////
    }
    for (int i = system.size ()-1; i >= 0; i--) {      
      Particle ps = system.get(i);
      
      ps.runDefault();
      if (ps.isDead()) {
        system.remove(i);
      }
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
  Particle(PVector l) {
    this.x = l.x;
    this.y = l.y;
    if ((int)random(2) == 0)  
      this.xDir =random(-2, 2);
    else
      this.yDir = random(-2, 2);
    this.lerpRand = random(0.01, 0.15);
    lifespan = 300.0;
    this.vel = random(15);
    this.mag = random(15);
    c = color(0, 255, 255);
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
    x = lerp(x, center.x, lerpRand);
    y = lerp(y, center.y, lerpRand);
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
    stroke(c, lifespan);
    strokeWeight(0.25);
    fill(c, lifespan);
    ellipse(this.x, this.y, 1, 1);
  }
  void updateDefault() {
    if (xDir != 0) {
      xDir += vel;
      y += mag * sin(yDir);
    } else yDir += vel;
    x += mag * sin(xDir);
    y += mag * sin(yDir);
    lifespan -= 20.0;
  }
  // Is the particle still useful?
  boolean isDead() {
    if (lifespan < 0.0) {
      return true;
    } else {
      return false;
    }
  }
}

