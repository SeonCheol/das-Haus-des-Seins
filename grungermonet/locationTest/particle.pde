class System {
  ArrayList<ParticleSystem> system;
  int lifeSpan = 50;
  color c;
  System() {
    system = new ArrayList<ParticleSystem>();
  }
  void add(PVector position) {
    ParticleSystem ps = new ParticleSystem(position);
    system.add(ps);
  }
  void setColor(color c) {
    this.c = c;
  }
  void run() {
    for (ParticleSystem ps : system) {
      ps.setColor(c);
      ps.addParticle();
    }
    lifeSpan -= 2; //
    for (int i = system.size ()-1; i >= 0; i--) {
      ParticleSystem ps = system.get(i);

      ps.run();
      if (ps.isDead()) {
        system.remove(i);
      }
    }

    //    sum.div(count);
    //    println(sum);
    //    stroke(255, 0, 0);
    //    strokeWeight(10);
    //    
    //    point(sum.x, sum.y);
  }
  boolean isDead() {//
    return (lifeSpan < 0.0);
  }
}

class ParticleSystem {
  ArrayList<Particle> particles;
  PVector origin;
  color c;
  int lifeSpan = 20;
  ParticleSystem(PVector position) {
    origin = new PVector(position.x, position.y);
    particles = new ArrayList<Particle>();
  }
  void setColor(color c)
  {
    this.c = c;
  }
  void addParticle() {
    particles.add(new Particle(origin, c));
  }

  void run() {
    lifeSpan -= 4;
    for (int i = particles.size ()-1; i >= 0; i--) {
      Particle p = particles.get(i);
      p.run();
      if (p.isDead()) {
        particles.remove(i);
      }
    }
  }
  boolean isDead() {
    return (lifeSpan < 0.0);
  }
}

// A simple Particle class
class Particle {
  PVector position;
  PVector velocity;
  PVector acceleration;
  color c;
  float lifespan;

  Particle(PVector l, color c) {
    acceleration = new PVector(0, 2);
    velocity = new PVector(random(-5, 5), random(-5, 5));
    position = new PVector(l.x, l.y, 0);
    this.c = c;
    lifespan = 255.0;
  }

  void run() {
    update();
    display();
  }

  // Method to update position
  void update() {
    velocity.add(acceleration);
    position.add(velocity);
    lifespan -= 25.0;
  }
  // Method to display
  void display() {
    stroke(c, lifespan);
    fill(c, lifespan);
    ellipse(position.x, position.y, 4, 4);
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
