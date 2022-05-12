#include <Servo.h>
Servo servo;
int angle =0;
int sensorValue=0;
const int analogOutPin = 4; // Analog output pin that the LED is attached to
String sprava = String(10);
int w = 300; //ziadana hodnota


void setup() {
  // put your setup code here, to run once:
    Serial.begin(9600);

      
    servo.attach(2);
    servo.write(0);
     delay(500); 
         servo.write(90);
     delay(500); 



}



void loop() {

  if (Serial.available() > 0)
    {
      nastavenie();
    }
  // put your main code here, to run repeatedly:
  sensorValue = analogRead(A0);
  // print out the value you read:
  Serial.print(sensorValue);
  Serial.print(";");
  Serial.println(angle);
  delay(500);        // delay in between reads for stability
  servo.write(angle);
}

void nastavenie(){
   analogWrite(analogOutPin, 255);
   w = Serial.parseInt();  
    Serial.println(w);  
    angle=w;
   
}
