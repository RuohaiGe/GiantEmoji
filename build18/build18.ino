#include <Servo.h>

Servo servo_lefteye;
Servo servo_righteye;
Servo servo_lefteyeball;
Servo servo_righteyeball;
Servo servo_lefteyebrow_first;
Servo servo_lefteyebrow_second;
Servo servo_righteyebrow_first;
Servo servo_righteyebrow_second;

int LEFTEYE_BALL = 0;
int RIGHTEYE_BALL = 1;
int LEFTEYE = 2;
int RIGHTEYE = 3;
int EYEBROW_LEFT_FIRST = 4;
int EYEBROW_LEFT_SECOND = 5;
int EYEBROW_RIGHT_FIRST = 6;
int EYEBROW_RIGHT_SECOND = 7;
int MOUTH = 8;

int PIN_LEFTEYE_BALL = 8;
int PIN_RIGHTEYE_BALL = 7;
int PIN_LEFTEYE = 10;
int PIN_RIGHTEYE = 9;
int PIN_EYEBROW_LEFT_FIRST = 5;
int PIN_EYEBROW_LEFT_SECOND = 6;
int PIN_EYEBROW_RIGHT_FIRST = 4;
int PIN_EYEBROW_RIGHT_SECOND = 3;
int PIN_MOUTH_M = 11;
int PIN_MOUTH_D = 12;
int PIN_MOUTH_S = 13;

int data[9];
int i;
int previous;

void setup() {
  Serial.begin(9600); // set the baud rate
  Serial.println("Ready"); // print "Ready" once
  servo_lefteye.attach(PIN_LEFTEYE);
  servo_righteye.attach(PIN_RIGHTEYE);
  servo_lefteyeball.attach(PIN_LEFTEYE_BALL);
  servo_righteyeball.attach(PIN_RIGHTEYE_BALL);
  servo_lefteyebrow_first.attach(PIN_EYEBROW_LEFT_FIRST);
  servo_lefteyebrow_second.attach(PIN_EYEBROW_LEFT_SECOND);
  servo_righteyebrow_first.attach(PIN_EYEBROW_RIGHT_FIRST);
  servo_righteyebrow_second.attach(PIN_EYEBROW_RIGHT_SECOND);
  servo_lefteyeball.write(0);
  servo_righteyeball.write(0);
  servo_lefteye.write(0);
  servo_righteye.write(0);
  servo_lefteyebrow_first.write(0);
  servo_lefteyebrow_second.write(0);
  servo_righteyebrow_first.write(0);
  servo_righteyebrow_second.write(0);
  pinMode(PIN_MOUTH_M,OUTPUT);
  pinMode(PIN_MOUTH_D,OUTPUT);
  pinMode(PIN_MOUTH_S,OUTPUT);
  digitalWrite(PIN_MOUTH_D, HIGH);
  digitalWrite(PIN_MOUTH_M, LOW);
  i = 0;
}

void loop() {
    if (Serial.available()) { // only send data back if data has been sent
      data[i] = Serial.read();
      Serial.println(data[i]); // send the data back in a new line so that it is not all one long line
      i = i + 1;
      delay(100); // delay for 1/10 of a second
    }
    servo_lefteyeball.write(data[LEFTEYE_BALL]);
    servo_righteyeball.write(data[RIGHTEYE_BALL]);
    servo_lefteye.write(data[LEFTEYE]);
    servo_righteye.write(data[RIGHTEYE]);
    servo_lefteyebrow_first.write(data[EYEBROW_LEFT_FIRST]);
    servo_lefteyebrow_second.write(data[EYEBROW_LEFT_SECOND]);
    servo_righteyebrow_first.write(data[EYEBROW_RIGHT_FIRST]);
    servo_righteyebrow_second.write(data[EYEBROW_RIGHT_SECOND]);
    if(data[MOUTH] != 0){
       digitalWrite(PIN_MOUTH_D, LOW);
       for(int n = 0; n < previous; n++) {
            digitalWrite(PIN_MOUTH_S, HIGH);
            delay(10);
            digitalWrite(PIN_MOUTH_S, LOW);
            delay(10);
       }
       digitalWrite(PIN_MOUTH_D, HIGH);
       for(int n = 0; n < data[MOUTH]*100; n++) {
            digitalWrite(PIN_MOUTH_S, HIGH);
            delay(10);
            digitalWrite(PIN_MOUTH_S, LOW);
            delay(10);
        }
    }     
    if (i == 9) {
      i = 0;
      Serial.println("STOP");
      previous = data[MOUTH]*100;
      data[MOUTH] = 0;
      delay(1000) ; 
    }
    delay(100); // delay for 1/10 of a second
}

