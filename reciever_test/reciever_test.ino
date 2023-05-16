#include "Servo.h"

// Change IREC to 1 else DPF to 0
#define IREC 0
#define V_PIN 7
#define F_PIN 8
#define N_PIN 9
#define E_PIN 11
#define CLOSE IREC ? 98 : 0  // DPF close =98    IREC close= 0
#define OPEN IREC ? 35 : 120 // DPF open = 35    IREC open = 120                        //Use E_pin / Ethanol for IREC valve

Servo v;
Servo f;
Servo n;
Servo e;

const int SIGNAL_PIN1 = 2;
const int SIGNAL_PIN2 = 3;
const int SIGNAL_PIN3 = 4;
const int SIGNAL_PIN4 = 6;

// Pin to receive the signal from the first Arduino
// Pin to control the buzzer

int num = 0;

// # Pins based on bits
// # VEN - 0
// # FIL - 1
// # NOX - 2
// # ETH - 3
// # 1 = OPEN, 0 = Close, X = Previous State/Doesnt Matter
// # Concept Behind This Code:
// # State      | DPF | IREC
// # ------------------------------------------
// # Close ALL  | 0000 | 00X0
// # Fire       | 0011 | 00X1
// # Abort      | 0010 | 00X0
// # Fill       | 0100 | 01X0
// # Vent       | 1000 | 10X0

void setup()
{
  Serial.begin(19200);
  // make sure we pin up at the beginnning
  pinMode(SIGNAL_PIN1, INPUT_PULLUP);
  pinMode(SIGNAL_PIN2, INPUT_PULLUP);
  pinMode(SIGNAL_PIN3, INPUT_PULLUP);
  pinMode(SIGNAL_PIN4, INPUT_PULLUP);

  pinMode(E_PIN, INPUT_PULLUP);
  pinMode(N_PIN, INPUT_PULLUP);
  pinMode(F_PIN, INPUT_PULLUP);
  pinMode(V_PIN, INPUT_PULLUP);

  e.attach(E_PIN);
  n.attach(N_PIN);
  f.attach(F_PIN);
  v.attach(V_PIN);

  e.write(CLOSE);
  n.write(CLOSE);
  f.write(CLOSE);
  v.write(CLOSE);

  delay(1000);
}

void loop()
{
  // initial num
  if (digitalRead(SIGNAL_PIN1) == HIGH)
  {
    e.write(90);
    n.write(90);
    f.write(90);
    v.write(90);
  } else
  {
    e.write(0);
    n.write(0);
    f.write(0);
    v.write(0);
  }

  //   unsigned num = 0;

  //   if (digitalRead(SIGNAL_PIN1) == HIGH)
  //     num | 1;
  //   if (digitalRead(SIGNAL_PIN1) == LOW)
  //     num & 14;
  //   if (digitalRead(SIGNAL_PIN2) == HIGH)
  //     num | 2;
  //   if (digitalRead(SIGNAL_PIN2) == LOW)
  //     num & 13;
  //   if (digitalRead(SIGNAL_PIN3) == HIGH)
  //     num | 4;
  //   if (digitalRead(SIGNAL_PIN3) == LOW)
  //     num & 11;
  //   if (digitalRead(SIGNAL_PIN4) == HIGH)
  //     num | 8;
  //   if (digitalRead(SIGNAL_PIN4) == LOW)
  //     num & 7;

  //   Serial.println(num);
  //   // that is bad MKAY
  //   if (num == 15)
  //   {
  //     e.write(CLOSE);
  //     n.write(CLOSE);
  //     f.write(CLOSE);
  //     v.write(CLOSE);
  //   }
  //   else
  //   {
  //     if (num & 1 > 0)
  //       e.write(OPEN);
  //     else
  //       e.write(CLOSE);
  //     if (num & 2 > 0)
  //       n.write(OPEN);
  //     else
  //       n.write(CLOSE);
  //     if (num & 4 > 0)
  //       f.write(OPEN);
  //     else
  //       f.write(CLOSE);
  //     if (num & 8 > 0)
  //       v.write(OPEN);
  //     else
  //       v.write(CLOSE);
  //   }

    Serial.print(" ");
    Serial.print(digitalRead(SIGNAL_PIN1) == HIGH);
    Serial.print(" ");
    Serial.print(digitalRead(SIGNAL_PIN2) == HIGH);
    Serial.print(" ");
    Serial.print(digitalRead(SIGNAL_PIN3) == HIGH);
    Serial.print(" ");
    Serial.println(digitalRead(SIGNAL_PIN4) == HIGH);
  }
