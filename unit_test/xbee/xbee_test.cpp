void setup() {
  Serial1.begin(9600);
}

void loop() {
  if (Serial1.available() > 3) {
    char buf[4];
    Serial1.readBytes(buf, 4);
    Serial1.println("");
    Serial1.println("Echo back from Arduino to XBee....");
    Serial1.print("'");
    Serial1.print(buf);
    Serial1.println("'");
  }
}