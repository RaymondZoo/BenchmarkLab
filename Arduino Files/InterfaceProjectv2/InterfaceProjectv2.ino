
#include <Wire.h> //allows communication over i2c devices
#include <LiquidCrystal_I2C.h> //allows interfacing with LCD screens
#include "max6675.h"

const float pressureIn = A0; //select the analog input pin for the first pressure transducer
const float pressureOut = A3; //select the analog input pin for the second pressure transducer
const float pressureZero = 102.4; //analog reading of pressure transducer at 0psi, should be 102.4 from formula conversion
const float pressureMax = 921.6; //analog reading of pressure transducer at 30psi
int pressuretransducermaxPSI = 30; //psi value of transducer being used
const int baudRate = 9600; //constant integer to set the baud rate for serial monitor
int sensorreadDelay = 1000; //integer to set the sensor read delay in milliseconds

float pressureInValue = 0; //variable to store the value coming from the pressure transducer
float pressureOutValue = 0; //variable to store the value coming from the pressure transducer
float pressureDifference = 0; //variable to store the value coming from the pressure transducer

//pressure calibration
float pressureZeroI;
float pressureZeroO;

//LCD setup
//const LiquidCrystal_I2C lcd(0x27, 16, 2); //sets the LCD I2C communication address; format(address, columns, rows)
//const String dataLabel1 = "PressureIn";
//const String dataLabel2 = "PressureOut";

//temperature sensor setup
int ktcSO = 8;
int ktcCS = 9;
int ktcCLK = 10;

MAX6675 ktc(ktcCLK, ktcCS, ktcSO);

void setup() //setup routine, runs once when system turned on or reset
{
  Serial.begin(baudRate); //initializes serial communication at set baud rate bits per second
  //lcd.init(); //initializes the LCD screen
  //lcd.init();
  //lcd.backlight();

  delay(500);

  //  if (Serial.available()) // if there is data coming
  // {
  //   String command = Serial.readStringUntil('\n'); 
  //   command.trim();
  //   if (command.substring(0, 2) == "sd")
  //   {
  //     sensorreadDelay = command.substring(3).toInt();
  //   }

  //   if (command.substring(0, 3) == "psi")
  //   {
  //     pressuretransducermaxPSI = command.substring(4).toInt();
  //   }

  // }
  //pinMode(13, OUTPUT); // set the digital pin as output:
  //Serial.print(dataLabel1);
  //Serial.print(",");
  //Serial.print(dataLabel2);
  //Serial.print(",");
  //Serial.println("PressureDifference");

  //calibration
  //pressureZeroI = analogRead(pressureIn);
  //pressureZeroO = analogRead(pressureOut);
}

void loop() //loop routine runs over and over again forever
{
  float singleIN = analogRead(pressureIn);
  float singleOUT = analogRead(pressureOut);
  if (Serial.available()) // if there is data coming
  {
    String command = Serial.readStringUntil('\n'); // read string until meet newline character
    command.trim();
    if (command.substring(0, 2) == "sd")
    {
      sensorreadDelay = command.substring(3).toInt();
    }
    if (command.substring(0, 3) == "psi")
    {
      pressuretransducermaxPSI = command.substring(4).toInt();
    }
    if (command == "recalibrate")
    {
      //Serial.println("reached");
      //digitalWrite(13, HIGH); // turn on LED
      pressureZeroI = singleIN;
      pressureZeroO = singleOUT;
      //delay(5000);
      //digitalWrite(13, LOW); // turn off LED
    }
  }
  pressureInValue = ((singleIN - pressureZeroI) * pressuretransducermaxPSI) / (pressureMax - pressureZeroI); //conversion equation to convert analog reading to psi
  pressureOutValue = ((singleOUT - pressureZeroO) * pressuretransducermaxPSI) / (pressureMax - pressureZeroO); //conversion equation to convert analog reading to psi
  pressureDifference = pressureOutValue - pressureInValue;

  /*
  lcd.setCursor(0, 0); //sets cursor to column 0, row 0
  lcd.print("I:"); //prints label
  lcd.print(pressureInValue, 2); //prints pressure value to lcd screen, 1 digit on float
  lcd.setCursor(8, 0); //sets cursor to column 0, row 0
  lcd.print("O:"); //prints label
  lcd.print(pressureOutValue, 2); //prints pressure value to lcd screen, 1 digit on float
  lcd.print("   "); //to clear the display after large values or negatives
  lcd.setCursor(0, 1);
  lcd.print("D:");
  lcd.print(pressureDifference, 2); //prints pressure value to lcd screen, 1 digit on float
  */

  Serial.print(pressureInValue); //prints value from previous line to serial
  Serial.print(","); //prints value from previous line to serial
  Serial.print(pressureOutValue); //prints value from previous line to serial
  Serial.print(","); //prints value from previous line to serial
  Serial.print(pressureDifference); //prints value from previous line to serial
  Serial.print(",");
  Serial.println(ktc.readCelsius());
  delay(sensorreadDelay); //delay in milliseconds between read values
}
