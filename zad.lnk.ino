#include <Servo.h>

Servo servo;
int angle =45;
int sensorValue=0;    //fotorezistor
const int analogOutPin = 4; // analagovy pin LED
int w = 300; //ziadana hodnota
//bool open = 0;   //premenna pre pociatocnu inicializaciu
float P = 1;
float I = 3;
bool start_stop = 0; // premenna pre spustanie regulacie, odosielanie

String message;

void setup() {
  
    Serial.begin(9600);
    servo.attach(2);
    servo.write(0);
    delay(500); 
}

void loop() {

  if (Serial.available() > 0)
    {
      nastavenie();
    }
  if (start_stop)
    {
    delay(500);        
    sensorValue = analogRead(A0);
  // poslanie intenzity a uhla
    Serial.print(sensorValue);
    Serial.print(";");
    Serial.println(angle);
    
  
    servo.write(angle);
    }
}

String getValue(String data, char separator, int index)
{
    int found = 0;
    int strIndex[] = { 0, -1 };
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    }
    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}

void nastavenie(){
   analogWrite(analogOutPin, 255);
   //w = Serial.parseInt();  
   message = Serial.readString();
   start_stop = (getValue(message, ';', 0)=="1");
   w = getValue(message, ';', 1).toInt();
   P = getValue(message, ';', 2).toFloat();
   I = getValue(message, ';', 3).toFloat();

   
   angle = w;
  // open = 1;
   
}
