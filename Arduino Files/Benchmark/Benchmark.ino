/*
   To Do:
   report new SD after start
   How to use temperature sensor
   Choose temperature or pressure sensor reading depending on what user chooses to connect to the port

   Start Sequence:
   Play
   Configure ports?
   Set time of start
   Begin



*/

#include <Elegoo_GFX.h>    // Core graphics library
#include <Elegoo_TFTLCD.h> // Hardware-specific library
#include <TouchScreen.h>
#include <TimeLib.h>

// The control pins for the LCD can be assigned to any digital or
// analog pins...but we'll use the analog pins as this allows us to
// double up the pins with the touch screen (see the TFT paint example).
#define LCD_CS A3 // Chip Select goes to Analog 3
#define LCD_CD A2 // Command/Data goes to Analog 2
#define LCD_WR A1 // LCD Write goes to Analog 1
#define LCD_RD A0 // LCD Read goes to Analog 0

#define LCD_RESET A4 // Can alternately just connect to Arduino's reset pin

// When using the BREAKOUT BOARD only, use these 8 data lines to the LCD:
// For the Arduino Uno, Duemilanove, Diecimila, etc.:
//   D0 connects to digital pin 8  (Notice these are
//   D1 connects to digital pin 9   NOT in order!)
//   D2 connects to digital pin 2
//   D3 connects to digital pin 3
//   D4 connects to digital pin 4
//   D5 connects to digital pin 5
//   D6 connects to digital pin 6
//   D7 connects to digital pin 7
// For the Arduino Mega, use digital pins 22 through 29
// (on the 2-row header at the end of the board).

// Assign human-readable names to some common 16-bit color values:
#define  BLACK   0x0000
#define BLUE    0x001F
#define RED     0xF800
#define GREEN   0x07E0
#define CYAN    0x07FF
#define MAGENTA 0xF81F
#define YELLOW  0xFFE0
#define WHITE   0xFFFF

// Color definitions
#define ILI9341_BLACK       0x0000      /*   0,   0,   0 */
#define ILI9341_NAVY        0x000F      /*   0,   0, 128 */
#define ILI9341_DARKGREEN   0x03E0      /*   0, 128,   0 */
#define ILI9341_DARKCYAN    0x03EF      /*   0, 128, 128 */
#define ILI9341_MAROON      0x7800      /* 128,   0,   0 */
#define ILI9341_PURPLE      0x780F      /* 128,   0, 128 */
#define ILI9341_OLIVE       0x7BE0      /* 128, 128,   0 */
#define ILI9341_LIGHTGREY   0xC618      /* 192, 192, 192 */
#define ILI9341_DARKGREY    0x7BEF      /* 128, 128, 128 */
#define ILI9341_BLUE        0x001F      /*   0,   0, 255 */
#define ILI9341_GREEN       0x07E0      /*   0, 255,   0 */
#define ILI9341_CYAN        0x07FF      /*   0, 255, 255 */
#define ILI9341_RED         0xF800      /* 255,   0,   0 */
#define ILI9341_MAGENTA     0xF81F      /* 255,   0, 255 */
#define ILI9341_YELLOW      0xFFE0      /* 255, 255,   0 */
#define ILI9341_WHITE       0xFFFF      /* 255, 255, 255 */
#define ILI9341_ORANGE      0xFD20      /* 255, 165,   0 */
#define ILI9341_GREENYELLOW 0xAFE5      /* 173, 255,  47 */
#define ILI9341_PINK        0xF81F

/******************* UI details */
#define BUTTON_X 280//40 +60+20 +60+20 
#define BUTTON_Y 25
#define BUTTON_W 60
#define BUTTON_H 30
#define BUTTON_SPACING_X 20
#define BUTTON_SPACING_Y 10
#define BUTTON_TEXTSIZE 1

// text box where numbers go
#define TEXT_X 10
#define TEXT_Y 10
#define TEXT_W 220
#define TEXT_H 50
#define TEXT_TSIZE 1
#define TEXT_TCOLOR BLACK
// the data (phone #) we store in the textfield
#define TEXT_LEN 19
char textfield[TEXT_LEN + 1] = "yyyy-mm-dd hh:mm:ss";
uint8_t textfield_i = 0;

#define YP A3  // must be an analog pin, use "An" notation!
#define XM A2  // must be an analog pin, use "An" notation!
#define YM 9   // can be a digital pin
#define XP 8   // can be a digital pin

//Touch For New ILI9341 TP
#define TS_MINY 120
#define TS_MAXY 900

#define TS_MINX 70
#define TS_MAXX 920
// We can have a status line, can be used for recalibration
#define STATUS_X 500
#define STATUS_Y 500

#include <SPI.h>             // f.k. for Arduino-1.5.2
#define USE_SDFAT
#include <SdFat.h>           // Use the SdFat library

#if SPI_DRIVER_SELECT != 2
#error edit SdFatConfig.h .  READ THE SKETCH INSTRUCTIONS
#endif

SoftSpiDriver<12, 11, 13> softSpi; //Bit-Bang on the Shield pins SDFat.h v2
SdFat SD;
#define SD_CS SdSpiConfig(10, DEDICATED_SPI, SD_SCK_MHZ(0), &softSpi)

File csvFile;


Elegoo_TFTLCD tft(LCD_CS, LCD_CD, LCD_WR, LCD_RD, LCD_RESET);
TouchScreen ts = TouchScreen(XP, YP, XM, YM, 300);
// If using the shield, all control and data lines are fixed, and
// a simpler declaration can optionally be used:
// Elegoo_TFTLCD tft;

Elegoo_GFX_Button buttons[5];
/* create 6 buttons */
char buttonlabels[5][10] = {"Start", "Pause", "Stop ", "NFile", "Recal"};
uint16_t buttoncolors[5] = {ILI9341_DARKGREEN, ILI9341_YELLOW, ILI9341_RED,
                            ILI9341_BLUE, ILI9341_PURPLE
                           };//ILI9341_MAGENTA

Elegoo_GFX_Button delayChange[2];
char delayLabels[2][10] = {"-", "+"};
uint16_t delayColors[2] = {ILI9341_RED, ILI9341_DARKGREEN};

Elegoo_GFX_Button numbers[15];
/* create 15 buttons, in classic candybar phone style */
char numberlabels[12][10] = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Enter", "Clear" };
uint16_t numbercolors[12] = {ILI9341_BLUE, ILI9341_BLUE, ILI9341_BLUE,
                             ILI9341_BLUE, ILI9341_BLUE, ILI9341_BLUE,
                             ILI9341_BLUE, ILI9341_BLUE, ILI9341_BLUE,
                             ILI9341_BLUE, ILI9341_DARKGREEN, ILI9341_RED
                            };


//new booleans for buttons
boolean reading = false;
boolean newStart = true;
String currentFile = "test1.csv";
int sensorDelay = 1000;
boolean newSD = false;
boolean timeInputted = false;

void setup(void) { //************************************************************************************************************************************************************************
  Serial.begin(9600);
  Serial1.begin(9600);
  //Serial.println(F("TFT LCD test")); --------------- All the Serial.printn() are commented out in order to avoid interfering with the Arduino communication

#ifdef USE_Elegoo_SHIELD_PINOUT
  //Serial.println(F("Using Elegoo 2.8\" TFT Arduino Shield Pinout"));
#else
  //Serial.println(F("Using Elegoo 2.8\" TFT Breakout Board Pinout"));
#endif

  //Serial.print("TFT size is "); Serial.print(tft.width()); Serial.print("x"); Serial.println(tft.height());

  tft.reset();

  uint16_t identifier = tft.readID();
  if (identifier == 0x9325) { //taken from phonecal example, open that file for the comments
  } else if (identifier == 0x9328) {
  } else if (identifier == 0x4535) {
  } else if (identifier == 0x7575) {
  } else if (identifier == 0x9341) {
  } else if (identifier == 0x8357) {
  } else if (identifier == 0x0101)
  {
    identifier = 0x9341;
  } else {
    identifier = 0x9341;

  }

  tft.begin(identifier);
  tft.setRotation(3); //2 is vertical
  tft.fillScreen(WHITE);

  // create buttons
  for (uint8_t row = 0; row < 5; row++) {
    buttons[row].initButton(&tft, BUTTON_X,
                            BUTTON_Y + row * (BUTTON_H + BUTTON_SPACING_Y), // x, y, w, h, outline, fill, text
                            BUTTON_W, BUTTON_H, ILI9341_WHITE, buttoncolors[row], ILI9341_WHITE,
                            buttonlabels[row], BUTTON_TEXTSIZE);
    buttons[row].drawButton();
  }

  for (uint8_t row = 0; row < 2; row++) {
    delayChange[row].initButton(&tft, 155 + (row * (25)), 80, 25, 25, ILI9341_WHITE, delayColors[row], ILI9341_WHITE, delayLabels[row], 1);
    delayChange[row].drawButton();
  }

  for (uint8_t row = 0; row < 4; row++) {
    for (uint8_t col = 0; col < 3; col++) {
      numbers[col + row * 3].initButton(&tft, 30 + col * (50 + 5), 120 + row * (25 + 5),
                                        50, 25, ILI9341_WHITE, numbercolors[col + row * 3], ILI9341_WHITE,
                                        numberlabels[col + row * 3], 1);
      numbers[col + row * 3].drawButton();
    }
  }

  // create log text box
  tft.drawRect(TEXT_X, TEXT_Y, TEXT_W, TEXT_H, BLACK);



  boolean good = SD.begin(SD_CS);
  if (!good) {
    Serial.print(F("cannot start SD"));
    while (1);
  }
  else {
    Serial.println("SD started successfully");
  }
  char namebuf[32] = "/";
  File root = SD.open(namebuf);
  int pathlen = strlen(namebuf);
  char *nm = namebuf + pathlen;
  SD.open(nm);

  while (SD.exists(currentFile))
  {
    //SD.remove(currentFile); // maybe make a new file instead of replacing old one
    currentFile = "test" + String(currentFile.substring(4, currentFile.indexOf(".")).toInt() + 1) + ".csv";
  }
  csvFile = SD.open(currentFile, FILE_WRITE);
  csvFile.close();

  tft.setCursor(TEXT_X + 2, TEXT_Y + 40);
  tft.setTextColor(TEXT_TCOLOR, WHITE);
  tft.setTextSize(TEXT_TSIZE);
  tft.print(currentFile); // current file display

  tft.setCursor(TEXT_X + 130, TEXT_Y + 40);
  tft.print("SD:" + String(sensorDelay) + " ms");// current sensor delay display

  tft.setCursor(40, 15);
  tft.print("Time: ");//current time display
  tft.setCursor(70, 15);
  tft.print(textfield);



}
void status(String msg) { //maybe add a counter that will hold the message for 2 seconds before clearing it? not important tbh
  tft.setCursor(TEXT_X + 2, TEXT_Y + 50);
  tft.setTextColor(TEXT_TCOLOR, WHITE);
  tft.setTextSize(0.5);
  tft.print(msg);
  tft.setCursor(TEXT_X + 2, TEXT_Y + 50);
  tft.print("                                     ");
}
void log(String str)
{
  tft.setCursor(TEXT_X + 2, TEXT_Y + 20);
  tft.setTextColor(TEXT_TCOLOR, WHITE);
  tft.setTextSize(TEXT_TSIZE);
  tft.print("                     ");
  tft.setCursor(TEXT_X + 2, TEXT_Y + 20);


  tft.print(str);
  csvFile = SD.open(currentFile, FILE_WRITE);
  csvFile.println(str); //need to add time to this *******
  csvFile.close();
}

int format(int one, int two)
{
  return (String(textfield[one]) + String(textfield[two])).toInt();
}

#define MINPRESSURE 10
#define MAXPRESSURE 1000
void loop(void) {
  /***************************************************************************************************************************************************************************
    /*TSPoint p;
    p = ts.getPoint();
  */

  digitalWrite(13, HIGH);
  TSPoint p = ts.getPoint(); // raw x and y values
  digitalWrite(13, LOW);

  // if sharing pins, you'll need to fix the directions of the touchscreen pins ****** not sure what this means/may be important
  //pinMode(XP, OUTPUT);
  pinMode(XM, OUTPUT);
  pinMode(YP, OUTPUT);
  //pinMode(YM, OUTPUT);

  // we have some minimum pressure we consider 'valid'
  // pressure of 0 means no pressing!

  // p = ts.getPoint();

  if (p.z > MINPRESSURE && p.z < MAXPRESSURE) {
    // scale from 0->1023 to tft.width KEEP THIS DONT DELETE
    //Serial.println(tft.width());// -------> 320
    //Serial.println(tft.height());// ------> 240
    //Serial.print(p.x); Serial.print(",");Serial.println(p.y);
    int tempx = p.x;
    int tempy = p.y;
    p.y = map(tempx, TS_MINX, TS_MAXX, 0, tft.height()); // LOOK IN NOTES FOR HOW I DID THIS
    p.x = map(tempy, TS_MINY, TS_MAXY, 0, tft.width());
    //Serial.print("("); Serial.print(p.x); Serial.print(", ");
    //Serial.println(p.y);
  }

  // go thru all the buttons, checking if they were pressed
  for (uint8_t b = 0; b < 5; b++) {
    if (buttons[b].contains(p.x, p.y)) {
      //Serial.print("Pressing: "); Serial.println(b);
      buttons[b].press(true);  // tell the button it is pressed
    } else {
      buttons[b].press(false);  // tell the button it is NOT pressed
    }
  }

  for (uint8_t b = 0; b < 2; b++) {
    if (delayChange[b].contains(p.x, p.y)) {
      //Serial.print("Pressing: "); Serial.println(b);
      delayChange[b].press(true);  // tell the button it is pressed
    } else {
      delayChange[b].press(false);  // tell the button it is NOT pressed
    }
  }

  for (uint8_t b = 0; b < 12; b++) {
    if (numbers[b].contains(p.x, p.y)) {
      //Serial.print("Pressing: "); Serial.println(b);
      numbers[b].press(true);  // tell the button it is pressed
    } else {
      numbers[b].press(false);  // tell the button it is NOT pressed
    }
  }

  for (uint8_t b = 0; b < 5; b++) { // FLOW LOOP TESTING CONTROL BUTTONS
    if (buttons[b].justReleased()) {
      // Serial.print("Released: "); Serial.println(b);
      buttons[b].drawButton();  // draw normal
    }

    if (buttons[b].justPressed()) {
      buttons[b].drawButton(true);  // draw invert!
      //button controls
      tft.setCursor(TEXT_X + 2, TEXT_Y + 20);
      tft.setTextColor(TEXT_TCOLOR, WHITE);
      tft.setTextSize(TEXT_TSIZE);

      if (b == 0)
      {
        if (!timeInputted)
        {
          status("Set the time using the number pad");
        }
        else
        {
          reading = true;

          if (newStart == true)
          {
            //csv header
            tft.print("PIn, POut, PDiff");
            csvFile = SD.open(currentFile, FILE_WRITE);
            csvFile.println("PressureIn, PressureOut, PressureDifference"); //not using log()because the strings aren't the same
            csvFile.close();
          }


          String str = "START";

          log(str);
        }
      }
      else if (b == 1)
      {
        reading = false;
        String str = "PAUSE";

        log(str);
      }
      else if (b == 2)
      {
        reading = false;
        String str = "STOP";

        newStart = true;

        log(str);
      }
      else if (b == 3)
      {
        if (!reading)
        {
          while (SD.exists(currentFile))
          {
            currentFile = "test" + String(currentFile.substring(4, currentFile.indexOf(".")).toInt() + 1) + ".csv";
            status("New file being created.");
          }
        }
        else
        {
          status("You must pause or stop the program");
        }
      }
      else if (b == 4)
      {
        Serial1.println("recalibrate");
        String str = "RECALIBRATING";

        log(str);

      }
    }
  }
  for (uint8_t b = 0; b < 2; b++) { //SENSOR DELAY BUTTONS
    if (delayChange[b].justReleased()) {
      // Serial.print("Released: "); Serial.println(b);
      delayChange[b].drawButton();  // draw normal
    }

    if (delayChange[b].justPressed()) {
      delayChange[b].drawButton(true);  // draw invert!
      if (!reading)
      {
        //newSD = true;
        String str = "NEW SD:";
        if (b == 0)
        {
          sensorDelay -= 1000;
          if (sensorDelay <= 0)
          {
            status("You cannot set a smaller sensor delay");
            sensorDelay = 1000;
          }
        }
        else if (b == 1)
        {
          sensorDelay += 1000;
        }
        //Serial1.println("sd "+String(sensorDelay)); // can report this at START
        log(str + String(sensorDelay));
        tft.setCursor(TEXT_X + 130, TEXT_Y + 40);
        tft.print("            ");
      }
      else
      {
        status("You must pause or stop the program");
      }
    }
  }

  if (!timeInputted)
  {
    for (uint8_t b = 0; b < 12; b++) {
      if (numbers[b].justReleased()) {
        numbers[b].drawButton();  // draw normal
      }

      if (numbers[b].justPressed()) {
        numbers[b].drawButton(true);  // draw invert!

        // if a numberpad button, append the relevant # to the textfield
        if (b >= 0 && b <= 10) {
          if (textfield_i < TEXT_LEN) {
            textfield[textfield_i] = numberlabels[b][0];
            textfield_i++;
            if (textfield_i == 4 || textfield_i == 7 || textfield_i == 10 || textfield_i == 13 || textfield_i == 16) //could've done if the textfield isn't numeric
            {
              textfield_i++;
            }
            textfield[textfield_i] = 0; // zero terminate, explained by c++
          }
        }

        // clr button! delete char
        if (b == 11) {

          textfield_i = 0;
          while (textfield_i < 20)
          {
            textfield[textfield_i] = "yyyy-mm-dd hh:mm:ss"[textfield_i];
            textfield_i++;
          }
          textfield_i = 0;
        }
        if (b == 10) {
          //hh,mm,ss,dd,mm, yyyy
          setTime(format(11, 12), format(14, 15), format(17, 18), format(0, 3), format(5, 6), format(8, 9));
          timeInputted = true;
          tft.fillRect(0, 100, 200, 250, WHITE);
        }

        // update the current text field
        tft.setCursor(70, 15);
        tft.setTextColor(TEXT_TCOLOR, WHITE);
        tft.setTextSize(TEXT_TSIZE);
        tft.print(textfield);

      }
    }
  }


  // update the current text field
  tft.setCursor(TEXT_X + 2, TEXT_Y + 40);
  tft.setTextColor(TEXT_TCOLOR, WHITE);
  tft.setTextSize(TEXT_TSIZE);
  tft.print(currentFile);//current file display

  tft.setCursor(TEXT_X + 130, TEXT_Y + 40);
  tft.print("SD:" + String(sensorDelay) + " ms"); // sensordelay display

  if (timeInputted)
  {

    tft.setCursor(70, 15);
    tft.print("                    "); //alternatively determine where the minimum time will end and erase that so that atleast the minimum is overwritten each time
    tft.setCursor(70, 15);
    tft.print(String(year()) + "-" + String(month()) + "-" + String(day()) + " " + String(hour()) + ":" + String(minute()) + ":" + String(second()));
    adjustTime(sensorDelay / 2000.0); // for double division
  }



  // if there is data coming
  if (Serial1.available())
  {

    String command = Serial1.readStringUntil('\n');
    Serial.println(command);
    if (reading)
    {
      tft.setCursor(TEXT_X + 2, TEXT_Y + 20);
      tft.print(command);
      csvFile = SD.open(currentFile, FILE_WRITE);
      csvFile.println(command); //need to add time to this***
      csvFile.close();
    }
  }

  //delay(10); // UI debouncing
}
