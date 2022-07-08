void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 3) {
    char buf[4];
    Serial.readBytes(buf, 4);
    Serial.println("");
    Serial.println("Echo back from Arduino to XBee....");
    Serial.print("'");
    Serial.print(buf);
    Serial.println("'");
  }
}