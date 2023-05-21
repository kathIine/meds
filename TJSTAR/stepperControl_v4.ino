#include <AccelStepper.h>

// Define stepper motor connections
#define LINEAR_STEP_PIN         3 //linear stepper is Y
#define LINEAR_DIR_PIN          6
#define LINEAR_ENABLE_PIN       8

#define TRAY_STEP_PIN         2 //tray stepper is X
#define TRAY_DIR_PIN          5
#define TRAY_ENABLE_PIN       8

#define Y_LIMIT_PIN           10
/*
#define X_STEP_PIN 2   // Step pin for X stepper motor
#define X_DIR_PIN 5    // Direction pin for X stepper motor

#define Y_STEP_PIN 3   // Step pin for Y stepper motor
#define Y_DIR_PIN 6    // Direction pin for Y stepper motor

#define Z_STEP_PIN 4   // Step pin for Z stepper motor
#define Z_DIR_PIN 7    // Direction pin for Z stepper motor

#define A_STEP_PIN 9   // Step pin for A stepper motor
#define A_DIR_PIN 12   // Direction pin for A stepper motor*/

// Initialize the stepper motor object
AccelStepper stepperLinear(1, LINEAR_STEP_PIN, LINEAR_DIR_PIN);
AccelStepper stepperTray(2, TRAY_STEP_PIN, TRAY_DIR_PIN);

void setup() {
  // Set the maximum speed and acceleration for the stepper motor
  stepperLinear.setMaxSpeed(1000);
  stepperLinear.setAcceleration(10000);

  stepperTray.setMaxSpeed(1000);
  stepperTray.setAcceleration(10000);

  // Set the enable pin to high to enable the stepper motor
  pinMode(LINEAR_ENABLE_PIN, OUTPUT);
  digitalWrite(LINEAR_ENABLE_PIN, HIGH);

  pinMode(TRAY_ENABLE_PIN, OUTPUT);
  digitalWrite(TRAY_ENABLE_PIN, HIGH);

  pinMode(Y_LIMIT_PIN, INPUT_PULLUP);
  
  Serial.begin(9600);
}

int topTrayValue = 1000;
int inBetweenSteps = 250;
int trayGearSize = 120;
int stepperGearSize = 60;
int stepMode = 2; //half steps
int dispenseOne = 6.25 * (trayGearSize * stepperGearSize) * stepMode;
int spd = 1000;

int stepsInRot = 800;
int traySlots = 32;

void shakeTray(){
  int trayStart = stepperTray.currentPosition();

  while(stepperLinear.distanceToGo() != 0){
    stepperTray.move(25);
    while(abs(stepperTray.distanceToGo()) != 0){
      stepperTray.run();
    }
    stepperTray.move(-25);
    while(abs(stepperTray.distanceToGo()) != 0){
      stepperTray.run();
    }
  }
  stepperTray.moveTo(trayStart);
}
int fastSpeed = 2000;
int slowSpeed = 1000;

void moveToTray(int trayNumber){
  //tray number goes from 1 to 4 (1 is the top)
  stepperLinear.setMaxSpeed(fastSpeed);

  int currentLocation = stepperLinear.currentPosition();

  int fourthTray = -2600; //at the bottom
  int thirdTray = fourthTray - 700;
  int secondTray = fourthTray - 1600;
  int firstTray = fourthTray - 2300;
  stepperTray.setEnablePin(-1);
  //Serial.println("trayNumber is " + String(trayNumber));
  int desiredPosition = 100;
  if(trayNumber == 1){
    desiredPosition = firstTray;
  }
  else if(trayNumber == 2){
    desiredPosition = secondTray;
  }
  else if(trayNumber == 3){
    desiredPosition = thirdTray;
  }
  else{
    desiredPosition = fourthTray;
  }
  stepperTray.setEnablePin(8);
  int moveAmount = desiredPosition - currentLocation;
  //stepperLinear.direction(-1)
  stepperLinear.move(moveAmount); //AMOUNT IS NEGATIVE TO GO THE RIGHT WAY
  while(abs(stepperLinear.distanceToGo()) != 0){
    stepperLinear.run();
  }
  delay(500); //wait a bit before turning thing to dispense
  stepperLinear.setMaxSpeed(slowSpeed);

}

void dispensePill(int amount){
  int steps1Rot = 800;
  int traySlots = 32;
  int gearRatio = 60 / 120; //60 on stepper, 120 on tray

  int amountToTurn = (steps1Rot / traySlots) * 2; //2 is the gear ratio
  for(int i = 0; i < amount; i++){
    //Serial.print("dispensed one");
    stepperTray.move(amountToTurn);
    while(abs(stepperTray.distanceToGo()) != 0){
      stepperTray.run();
    }
    delay(500); //slightly delays after each dispense
  }
}

void resetLinearStepper(){
  unsigned long interval = 10;
  static unsigned long timer = 0;

  stepperLinear.move(10000);
  while(digitalRead(Y_LIMIT_PIN) == 0){
    stepperLinear.run();
  }
  stepperLinear.stop();
  //Serial.println("clicked");
  
  //moving up a bit slowly
  stepperLinear.move(-250);
  //while(digitalRead(Y_LIMIT_PIN) == 1){
  //  stepperLinear.run();
  //}
  while(abs(stepperLinear.distanceToGo()) != 0 || digitalRead(Y_LIMIT_PIN) == 1){
    stepperLinear.run();
  }
  stepperLinear.stop();
  delay(500);

  //moving back down slowly to click
  stepperLinear.setMaxSpeed(200);
  stepperLinear.move(1000);
  while(digitalRead(Y_LIMIT_PIN) == 0){
    stepperLinear.run();
  }
  stepperLinear.stop();
  delay(500);
  stepperLinear.setCurrentPosition(0);
  //Serial.println("second click");
}

int start = 0;

void loop() {
  // Move the stepper motor forward

  //constantly reading data from serial communication with raspberry pi
  //soucre: https://docs.arduino.cc/built-in-examples/strings/StringToInt
  //data format: [Tray][delimiter][Amount]'\n'
  
  //leave gear stepper disabled with no holding torque
  if(start == 0){
    Serial.println("Resetting stepper");
    resetLinearStepper();
    start = 1;
  }
  
  char delimiter = ' ';
  String currString = "";
  int trayData = 0;
  int amountData = 0;
  bool dispense = false;
  if(Serial.available() > 0){
    while(Serial.available() && amountData == 0){
      char currChar = Serial.read(); //read character
      //Serial.print(currChar);
      currString += (char)currChar;
      if(currChar == delimiter){
        trayData = currString.toInt();
        Serial.println(trayData);
        currString = "";
      }
      if(currChar == '\n'){
        amountData = currString.toInt();
        //Serial.println(amountData);
        currString = "";
        dispense = true;
      }
    }
  }

  //if both pieces of information have been recieved move the steppers
  if(dispense == true){
    Serial.print("recieved both");
    Serial.print(String(trayData) + " " + String(amountData));
    Serial.println("\n"); 
    //resetLinearStepper();
    moveToTray(trayData);
    dispensePill(amountData);
    resetLinearStepper(); //reset after dispensing (go to bottom)
    trayData = 0;
    amountData = 0;
    dispense = false;
  }
  delay(100);
}
