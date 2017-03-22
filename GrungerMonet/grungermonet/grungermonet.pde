BufferedReader reader;
String line;
char []c;

void setup() {
  size(200, 200);
  // Starts a myServer on port 5204
  reader = createReader("test.txt");
}

void draw() {
  try {
    String t = "";
    line = reader.readLine();
    if (line == null) {
      // Stop reading because of an error or file is empty
      noLoop();  
      reader.close();
    } else {
      int i=0;
      char tmp = line.charAt(i);      
      while (true) {
        try {
          println(tmp);
          tmp = line.charAt(++i);
          if 
        } 
        catch(Exception e) {
          break;
        }
      }
    }
  } 
  catch (IOException e) {
    e.printStackTrace();
    line = null;
  }
}