import processing.net.*; 

//Client myClient; 
//double dataIn; 
//String k = "";

//void setup() { 
//  size(200, 200); 
//  // Connect to the local machine at port 5204.
//  // This example will not run if you haven't
//  // previously started a server on this port.
//  myClient = new Client(this, "127.0.0.1", 5810);
//} 

//void draw() { 
//  if (myClient.available() > 0) { 
//    k = myClient.readString();
//  } 
//  //String k = String.valueOf(dataIn);
//  println(k);
//  background((int)dataIn);
//} 


Server myServer;
int val = 0;

void setup() {
  size(200, 200);
  // Starts a myServer on port 5204
  myServer = new Server(this, 5204); 
}

void draw() {
  val = (val + 1) % 255;
  background(val);
  myServer.write(val);
}