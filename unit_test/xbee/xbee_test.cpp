const unit8_t END = 0xC0;
const unit8_t ESC = 0xDB;
const unit8_t ESC_END = 0xDC;
const unit8_t ESC_ESC = 0xDD;

union Data {
  int phase;
  int light;
  int jump;
  float press;
  float lati;
  float longi;
  float alti;
  float magX;
  float magY;
  unit8_t b[36];
}

void setup() {
  Serial1.begin(9600);
  Serial1.println("%5s|%5s|%5s|%8s|%8s|%8s|%8s|%8s|%8s", "phase", "light", "jump", "press", "lati", "longi", "alti", "magX", "magY");
}

void loop() {
  if (Serial1.available() > 53) {
    // phase(int,1byte),light(int,4byte),jump(int,1byte),pressure(double,8byte),latitude(double,8byte),longitude(double,8byte),altitude(double,8byte),magX(double,8byte),magY(double,8byte)
    char buf[54];
    Serial1.readBytes(buf, 54);

    int phase = buf[0];

    string light_str = {buf[1], buf[2], buf[3], buf[4]};
    int light = stoi(light_str, nullptr, 8);

    int jump = buf[5];

    string press_str = {buf[6], buf[7], buf[8], buf[9], buf[10], buf[11], buf[12], buf[13]};
    double press = strtod(press_str);

    string lati_str = {buf[14], buf[15], buf[16], buf[17], buf[18], buf[19], buf[20], buf[21]};
    double lati = strtod(lati_str);

    string longi_str = {buf[22], buf[23], buf[24], buf[25], buf[26], buf[27], buf[28], buf[29]};
    double longi = strtod(longis_str);

    string alti_str = {buf[30], buf[31], buf[32], buf[33], buf[34], buf[35], buf[36], buf[37]};
    double alti = strtod(alti_str);

    string magX_str = {buf[38], buf[39], buf[40], buf[41], buf[42], buf[43], buf[44], buf[45]};
    double magX = strtod(magX_str);

    string magY_str = {buf[46], buf[47], buf[48], buf[49], buf[50], buf[51], buf[52], buf[53]};
    double magY = strtod(magY_str);

    Serial1.println("%5d|%5d|%5d|%8f|%8f|%8f|%8f|%8f|%8f", phase, light, jump, press, lati, longi, alti, magX, magY);
}