#include <Wire.h>

#define NicromOn LOW
#define NicromOff HIGH

const int SLAVE_ADDRESS = 0x8;

const int CdsPin = A0;
const int JumperPin = 13;
const int Ni = 2;

int CdsVal = 0;
int JumperVal = 0;
byte data[5];
char phase;

void setup() {
  Serial1.begin(9600);

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
  while(Wire.available()) {
    char c = Wire.read();
    switch(c) {
      case 0x0:
        digitalWrite(Ni, NicromOn);
        break;
      case 0x1:
        digitalWrite(Ni, NicromOff);
        break;
      case 0x2:
        phase = Wire.read();
        Serial1.print("phase");
        Serial1.print(phase+'0');
        Serial1.println("start");
        break;
      case 0x3:
        phase = Wire.read();
        Serial1.print("phase");
        Serial1.print(phase+'0');
        Serial1.println("finish");
        break;
      case 0x4:
        break;
    }
  }
}


void loop() {
}