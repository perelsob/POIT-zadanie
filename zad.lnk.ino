#include <Servo.h>

Servo servo;
int angle =0;
int sensorValue=0;    //fotorezistor
const int analogOutPin = 4; // analagovy pin LED
int w = 0; //ziadana hodnota
//parametre regulatora
float P = 0.04;     
float I = 0.02;
bool start_stop = 0; // premenna pre spustanie regulacie, odosielanie
bool open_bool = 0;  //inicializacia, deaktivacia
float y = 0;    //vystupna intenzita

unsigned long currentTime, previousTime;
double elapsedTime;
float error;
float lastError;
float cumError;

String message;   

//testovacia sprava 1;70;0.0001;0.0002

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
  if (start_stop && open_bool)
    {
      vypis();    
      Serial.print(";");
      Serial.print(0); //premenna pre zapis  
      Serial.println(";");
      regulacia();
      servo.write(angle);
    }
}

void regulacia(){
  currentTime = millis();
  
  elapsedTime = (double)(currentTime - previousTime);        //compute time elapsed from previous computation
  error = w - y;                                // determine error
  cumError += error * elapsedTime;                // compute integral
  angle = P*error + I*cumError;                //PI output               
  lastError = error;                                //remember current error
  previousTime = currentTime;  

//ohranicenie akcneho zasahu
  if (angle>90)
    {angle = 90;}
  else if(angle<0)
    {angle = 0;}
  
}

void vypis()
{
    delay(500); 
    sensorValue = analogRead(A0);
    y = map(sensorValue,180,670,0,100); //prepocitanie intenzity na percenta
    if (y>100)  //ohranicenie
      {y = 100;}
    else if (y<0)
      {y = 0;}
  // poslanie intenzity a uhla
    Serial.print(w);
    Serial.print(";");
    Serial.print(y);
    Serial.print(";");
    Serial.print(angle);
  }
//funkcia pre rozsekanie prijatych sprav
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
   
   cumError =0; //vynulovanie komulativnej chyby
 
   message = Serial.readString();
   open_bool = (getValue(message, ';', 0)=="1");
   start_stop = (getValue(message, ';', 1)=="1");
   w = getValue(message, ';', 2).toInt();
   P = getValue(message, ';', 3).toFloat();
   I = getValue(message, ';', 4).toFloat();

   if(open_bool)
   {
    analogWrite(analogOutPin, 255);

    if (start_stop==0)
      {
      vypis();
      Serial.print(";");
      Serial.print(1); //premenna pre zapis
      Serial.println(";");
      }
   }

   else
   {
    analogWrite(analogOutPin, 0);
    servo.write(0);
    }

  
   
}
