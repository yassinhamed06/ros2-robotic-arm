#include <Servo.h>

Servo servo1;
Servo servo2;

float current1 = 90;
float current2 = 90;

float start1 = 90;
float start2 = 90;

int target1 = 90;
int target2 = 90;

unsigned long startTime = 0;
unsigned long duration = 3000;

bool moving = false;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(50);

  servo1.write(90);
  servo2.write(90);

  servo1.attach(9);
  servo2.attach(10);
}

void loop() {

  if (moving) {

    float progress =
      (float)(millis() - startTime) / duration;

    if (progress >= 1.0) {
      progress = 1.0;
      moving = false;
    }

    current1 = start1 + (target1 - start1) * progress;
    current2 = start2 + (target2 - start2) * progress;

    servo1.write(round(current1));
    servo2.write(round(current2));
  }

  if (Serial.available() > 0) {

    String data = Serial.readStringUntil('\n');
    data.trim();

    int angle1, angle2;
    long timeMs;
    char extra;

    if (sscanf(data.c_str(), "%d,%d,%ld%c",
        &angle1, &angle2, &timeMs, &extra) == 3) {

      if (angle1 >= 45 && angle1 <= 135 &&
          angle2 >= 45 && angle2 <= 135 &&
          timeMs >= 1000 && timeMs <= 10000) {

        start1 = current1;
        start2 = current2;

        target1 = angle1;
        target2 = angle2;

        duration = timeMs;
        startTime = millis();

        moving = true;

        Serial.println("OK");

      } else {
        Serial.println("ERROR");
      }

    } else {
      Serial.println("ERROR");
    }
  }
}
