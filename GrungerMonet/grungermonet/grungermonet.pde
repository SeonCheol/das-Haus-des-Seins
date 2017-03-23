BufferedReader reader;
String line;
String [] c;
void setup() {
  size(200, 200);
  // Starts a myServer on port 5204
}
void draw() {
  try {
    reader = createReader("dataForsoundInfo0.txt");
    line = reader.readLine();
    if (line == null) {
      // Stop reading because of an error or file is empty
      noLoop();  
      reader.close();
    } else {
      c = split(line, " ");

      for (int i=0; i<c.length; i++) {
        float d = float(c[i]);
        println(d);
      }
      println(c[3]);
      reader.close();
    }
  }
  catch (IOException e) {
    e.printStackTrace();
    line = null;
  }
  catch (NullPointerException e) {
    e.printStackTrace();
  }
}