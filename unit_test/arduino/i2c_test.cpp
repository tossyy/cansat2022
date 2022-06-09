#include <Wire.h>

const int SLAVE_ADDRESS = 0x8;

const int CdsPin = A1;
const int JumperPin = 6;

int CdsVal = 0;
int JumperVal = 0;
byte data[5];

void setup() {
  pinMode(CdsPin, INPUT);
  pinMode(JumperPin, INPUT);
  
  Wire.begin(SLAVE_ADDRESS);
  Wire.onRequest(requestEvent);
}

void requestEvent() {
  CdsVal = analogRead(CdsPin);
  JumperVal = digitalRead(JumperPin);
  data[0] = byte{(CdsVal>>(8*3))&((1<<8)-1)};
  data[1] = byte{(CdsVal>>(8*2))&((1<<8)-1)};
  data[2] = byte{(CdsVal>>(8*1))&((1<<8)-1)};
  data[3] = byte{(CdsVal>>(8*0))&((1<<8)-1)};
  data[4] = byte{JumperVal == HIGH};
  Wire.write(data, 5);
}

void loop() {
}
