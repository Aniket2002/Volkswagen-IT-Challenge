#include <Adafruit_LiquidCrystal.h>
#define gasBefore A0
#define gasAfter A1
#define buzzer 4

Adafruit_LiquidCrystal lcdDisp(0);

void setup()
{
  lcdDisp.begin(16, 2);
  lcdDisp.print("Device ON");
  delay(2000);
  pinMode(gasBefore,INPUT);
  pinMode(gasAfter,INPUT);
  pinMode(buzzer,OUTPUT);
  digitalWrite(buzzer,LOW);
  Serial.begin(9600);
  lcdDisp.setCursor(0, 0);
  lcdDisp.print("Efficiency");
}

void loop()
{
  int valBefore = analogRead(gasBefore);
  int valAfter = analogRead(gasAfter);
  valBefore = map(valBefore, 85, 360, 0, 100);
  valAfter = map(valAfter, 85,360, 0, 100);
  Serial.print("Value Before: ");
  Serial.print(valBefore);
  Serial.print("    Value After: ");
  Serial.println(valAfter);
  int diff = valBefore-valAfter;
  float efficiency = (float)diff/(float)valBefore;
  efficiency = efficiency*100;
  Serial.print("Efficiency: ");
  Serial.print(efficiency);
  Serial.println("%");
  lcdDisp.setCursor(0, 1);
  lcdDisp.print(efficiency);
  if(efficiency < 70)
    digitalWrite(buzzer,HIGH);
  else
    digitalWrite(buzzer,LOW);
  
  delay(1000);
}