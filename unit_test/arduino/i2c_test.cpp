#include <Wire.h>

#define NicromOn LOW
#define NicromOff HIGH

const int SLAVE_ADDRESS = 0x8;

const int CdsPin = A1;
const int JumperPin = 6;
const int Ni = 2;

int CdsVal = 0;
int JumperVal = 0;
byte data[5];

void setup() {
  pinMode(CdsPin, INPUT);
  pinMode(JumperPin, INPUT);
  pinMode(Ni, OUTPUT);

  digitalWrite(Ni, NicromOff);
  
  Wire.begin(SLAVE_ADDRESS);
  Wire.onRequest(requestEvent);
  Wire.onReceive(recieveEvent);
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

void recieveEvent(int bitstream) {
  digitalWrite(Ni, NicromOn);
  delay(3000);
  digitalWrite(Ni, NicromOff);
}


void loop() {
  digitalWrite(Ni, NicromOff)
}