int pMinMass = 2;
int pMaxMass = 8;
int cMinMass = 15;
int cMaxMass = 100;

float waterfallMin;
float waterfallMax;

ArrayList<Particle> particles = new ArrayList<Particle>();
ArrayList<Collision> collisions = new ArrayList<Collision>();

boolean do_aabb_collision(float ax, float ay, float Ax, float Ay, float bx, float by, float Bx, float By) {
  return ! ((Ax < bx) || (Bx < ax) || (Ay < by) || (By < ay));
}

class Rainy {
  PVector pos;
  PVector vel;  
  PVector acc;
  float mass;
  color displayColor;
  float fallRate;

  Rainy(float x, float y, float mass, color displayColor) {
    this.pos = new PVector(x, y);
    this.vel = new PVector(0, 0);
    this.acc = new PVector(0, 0);
    this.mass = mass;
    this.fallRate = map(this.mass, pMinMass, pMaxMass, .1, .05);
  }

  float [] getBoundingBox() {
    float radius = mass / 2;
    int offset = 2;
    float returnArr[] = new float[4];

    returnArr[0] = this.pos.x - radius - offset;
    returnArr[1] = this.pos.y-radius-offset;
    returnArr[2] = this.pos.x+radius+offset;    
    returnArr[3] = this.pos.y+radius+offset;

    return returnArr;
  }

  void move() {
    PVector gravity = new PVector(0, this.fallRate);
    this.acc.add(gravity);
    this.vel.add(this.acc);
    this.pos.add(this.vel);
    this.acc.mult(0);
  }

  boolean resolveCollisions() {
    boolean hit_object = false;
    float bb1[] = this.getBoundingBox();

    for ( int c=0; c<collisions.size (); c++) {
      Collision col = collisions.get(c);
      float bb2[] = col.getBoundingBox();
      boolean is_close_enough = do_aabb_collision(bb1[0], bb1[1], bb1[2], bb1[3], 
      bb2[0], bb2[1], bb2[2], bb2[3]);

      if (is_close_enough) {
        float distance = dist(this.pos.x, this.pos.y, col.pos.x, col.pos.y);

        if ( distance < col.mass/2 ) {
          PVector offset = new PVector(this.pos.x, this.pos.y);
          offset.sub(col.pos);
          offset.normalize();
          offset.mult(col.mass/2 - distance);
          this.pos.add(offset);
          float friction = 1;
          float dampening = map(this.mass, pMinMass, pMaxMass, 1, .8);
          float mag = this.vel.mag();

          // Get its new vector.
          PVector bounce = new PVector(this.pos.x, this.pos.y);
          bounce.sub(col.pos);
          bounce.normalize();
          bounce.mult(mag*friction*dampening/3);
          this.vel = bounce;

          if (this.mass > 2) {
            this.mass = max(1, this.mass - 2);
            float splitCount =  1;
            for (int s = 0; s<splitCount; s++) {
              float mass = max(1, this.mass-1);
              color displayColor = color(255, 128, 64);

              Particle splash = new Particle(this.pos.x, this.pos.y, mass, displayColor);

              splash.vel = new PVector(this.vel.x, this.vel.y);
              splash.vel.rotate(radians(random(-45, 45)));
              splash.vel.mult(random(.6, .9));

              particles.add( splash);
            }
          }
          hit_object = true;
          break;
        }
      }
    }
    return hit_object;
  }

  void display() {
    //stroke(this.displayColor);
    stroke(255);
    strokeWeight(1);
    fill(255, 128, 64);
    ellipse(this.pos.x, this.pos.y, 8, 8);
  }
}







////****///
class Collision {
  PVector pos;
  PVector target;
  float mass;
  float targetMass;

  Collision(float x, float y, float mass) {
    this.pos = new PVector(x, y);
    this.target = new PVector(x, y);
    this.mass = mass;
    this.targetMass = mass;
  }

  float []getBoundingBox() {
    float radius = this.mass / 2;
    float []returnVal = {
      this.pos.x-radius, this.pos.y-radius, this.pos.x+radius, this.pos.y+radius
    };
    return returnVal;
  }

  void move() {
    this.pos = PVector.lerp(this.pos, this.target, .01);
    this.mass = lerp(this.mass, this.targetMass, .01);
  }

  void display() {
    noStroke();
    fill(255);
    ellipse(this.pos.x, this.pos.y, this.mass, this.mass);

    fill(0);
    ellipse(this.pos.x, this.pos.y, this.mass * .95, this.mass * .95);
  }
}





















