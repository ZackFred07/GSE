#include "Servo.h"

#define IREC 0
#define E_PIN 5
#define F_PIN 7
#define N_PIN 12
#define CLOSE IREC ? 98 : 0  // DPF close =98    IREC close= 0
#define OPEN IREC ? 35 : 120 // DPF open = 35    IREC open = 120                        //Use E_pin / Ethanol for IREC valve

Servo e;
Servo n;
Servo f;

const int SIGNAL_PIN1 = 10;
const int SIGNAL_PIN2 = 5;
const int SIGNAL_PIN3 = 3;

// Pin to receive the signal from the first Arduino
// Pin to control the buzzer

int num = 0;

void setup()
{
  Serial.begin(19200);
  // make sure we pin up at the beginnning
  pinMode(SIGNAL_PIN1, INPUT_PULLUP);
  pinMode(SIGNAL_PIN2, INPUT_PULLUP);
  pinMode(SIGNAL_PIN3, INPUT_PULLUP);

  pinMode(E_PIN, INPUT_PULLUP);
  pinMode(N_PIN, INPUT_PULLUP);
  pinMode(F_PIN, INPUT_PULLUP);

  e.attach(E_PIN);
  n.attach(N_PIN);
  f.attach(F_PIN);

  e.write(CLOSE);
  n.write(CLOSE);
  f.write(CLOSE);

  delay(1000);
}

void loop()
{
  // initial num
  num = 0;

  if (digitalRead(SIGNAL_PIN1) == HIGH)
    num | 4;
  if (digitalRead(SIGNAL_PIN1) == LOW)
    num & 3;
  if (digitalRead(SIGNAL_PIN2) == HIGH)
    num | 2;
  if (digitalRead(SIGNAL_PIN2) == LOW)
    num & 5;
  if (digitalRead(SIGNAL_PIN3) == HIGH)
    num | 1;
  if (digitalRead(SIGNAL_PIN3) == LOW)
    num & 6;

  switch (num)
  {
  case 1:
    e.write(OPEN);
    break;
  case 2:
    n.write(OPEN);
    break;
  case 3:
    e.write(OPEN);
    n.write(OPEN);
    break;
  case 4:
    f.write(OPEN) break;

  default: // Bad/ great safety
    e.write(CLOSE);
    n.write(CLOSE);
    f.write(CLOSE);
    break;
  }
  Serial.print(" ");
  Serial.print(digitalRead(SIGNAL_PIN1) == HIGH);
  Serial.print(" ");
  Serial.print(digitalRead(SIGNAL_PIN2) == HIGH);
  Serial.print(" ");
  Serial.println(digitalRead(SIGNAL_PIN3) == HIGH);
}
