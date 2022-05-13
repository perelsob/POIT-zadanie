#include <Servo.h>

Servo servo;
int angle =45;
int sensorValue=0;    //fotorezistor
const int analogOutPin = 4; // analagovy pin LED
int w = 300; //ziadana hodnota
bool open = 0;   //premenna pre zacatie posielania dat



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
  if (open)
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

void nastavenie(){
   analogWrite(analogOutPin, 255);
   w = Serial.parseInt();  
    
   angle = w;
   open = 1;
   
}
