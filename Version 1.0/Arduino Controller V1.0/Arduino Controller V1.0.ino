/*  
--------------------
    Version 1.0
--------------------
Gets song's title and displays it on the 20*4
LCD display. If song's title is smaller than 
21 characters then it is displayed on the
center of the display. Otherwise, the title
scrolls on the second line of the screen.
----------------------------------------------
            Issues:
-None at the moment
----------------------------------------------
            ToDo:
-Make it so it can process multiple data through
the serial port so it can also read date/time 
and maybe artist if theres space on screen.
Add a new void which will split the string
sent by the serial and split it accordingly
to a delimiter and then store the data to
a global array so they can be accessed for
displaying them.
*/
#include <LiquidCrystal_I2C.h>
#include <Wire.h> 
//Define lcd monitor
LiquidCrystal_I2C lcd(0x27,20,4);
//          Variables
int Li          = 20;
int Lii         = 0; 

String readSong = "";
String oldSong = "wesrctfvygbhunjimkl";
String data;

int wherePrint;
bool scrolling = false;
//Setup lcd display and serial port
void setup() {
  // initializing the LCD.
  lcd.init();
  lcd.backlight();
  // initializing the serial monitor.
  Serial.begin(9600);
}
//Scrolls the text if > 20 characteres
String Scroll_LCD_Left(String StrDisplay){
  lcd.setCursor(0, 1);
  String result;
  String StrProcess = StrDisplay + "      " + StrDisplay;
  result = StrProcess.substring(Li,Lii);
  Li++;
  Lii++;
  //Only God knows what's happening here
  if (Li>(StrProcess.length() - (StrDisplay.length() - 20))){
    Li=20;
    Lii=0;
  }
  return result;
}
//Main void loop
void loop() {
  //Get data from python server
  readSong = Serial.readString();
  if (readSong != ""){
    //Test if song changed
    if (readSong != oldSong){
      oldSong = readSong;
      lcd.clear();
      //Print the results
      if (readSong.length() < 20){
        wherePrint = (20 - (readSong.length())) / 2;
        lcd.setCursor(wherePrint, 1);
        lcd.print(readSong);
        //Disable text scrolling
        scrolling = false;
      }else{
        data = readSong;
        Li = 20;
        Lii = 0;
        //Enable text scrolling
        scrolling = true;
        
      }
    }
  }
  //Text scrolling switch
  if (scrolling){
    lcd.print(Scroll_LCD_Left(data));
  }

}