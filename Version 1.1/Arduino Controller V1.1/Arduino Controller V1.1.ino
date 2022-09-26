/*  
--------------------
    Version 1.1
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
-When spotify is not running display day and 
time at the center of the screen

-M̶a̶k̶e̶ i̶t̶ s̶o̶ i̶t̶ c̶a̶n̶ p̶r̶o̶c̶e̶s̶s̶ m̶u̶l̶t̶i̶p̶l̶e̶ d̶a̶t̶a̶ t̶h̶r̶o̶u̶g̶h̶ 
t̶h̶e̶ s̶e̶r̶i̶a̶l̶ p̶o̶r̶t̶ s̶o̶ i̶t̶ c̶a̶n̶ a̶l̶s̶o̶ r̶e̶a̶d̶ d̶a̶t̶e̶/t̶i̶m̶e̶  
a̶n̶d̶ m̶a̶y̶b̶e̶ a̶r̶t̶i̶s̶t̶ i̶f̶ t̶h̶e̶r̶e̶s̶ s̶p̶a̶c̶e̶ o̶n̶ s̶c̶r̶e̶e̶n̶. 
A̶d̶d̶ a̶ n̶e̶w̶ v̶o̶i̶d̶ w̶h̶i̶c̶h̶ w̶i̶l̶l̶ s̶p̶l̶i̶t̶ t̶h̶e̶ s̶t̶r̶i̶n̶g̶ s̶e̶n̶t̶ 
b̶y̶ t̶h̶e̶ s̶e̶r̶i̶a̶l̶ a̶n̶d̶ s̶p̶l̶i̶t̶ i̶t̶ a̶c̶c̶o̶r̶d̶i̶n̶g̶l̶y̶ t̶o̶ a̶ d̶e̶l̶i̶m̶i̶t̶e̶r̶ 
a̶n̶d̶ t̶h̶e̶n̶ s̶t̶o̶r̶e̶ t̶h̶e̶ d̶a̶t̶a̶ t̶o̶ a̶ g̶l̶o̶b̶a̶l̶ a̶r̶r̶a̶y̶ s̶o̶ t̶h̶e̶y̶ c̶a̶n̶ 
b̶e̶ a̶c̶c̶e̶s̶s̶e̶d̶ f̶o̶r̶ d̶i̶s̶p̶l̶a̶y̶i̶n̶g̶ t̶h̶e̶m̶.
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
String oldTime = "wesrctfvygbhunjimkl";
String data;
String delimiter = "sgxdfgchjkl";

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
//Split two different data types
String* ProcessData(String sentData){
  if (sentData.startsWith(delimiter)){
    String time = sentData.substring(11, 16);
    String song = sentData.substring(16, sentData.length());
    //Can anyone explain me why use String* and not String?
    String* songandtime = new String[2];
    songandtime[0] = song;
    songandtime[1] = time;
    return songandtime;
  }else{
    String* songandtime = new String[2];
    songandtime[0] = sentData;
    songandtime[1] = "";
    return songandtime;    
  }
  
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
    String* processedData = ProcessData(readSong);
    //Test if song changed
    if (processedData[1] != ""){
      if (processedData[1] != oldTime){
        oldTime = processedData[1];

        //lcd.clear();
        lcd.setCursor(0, 3);
        lcd.print("                    ");

        lcd.setCursor(15, 3);
        lcd.print(processedData[1]);
      }
    }
    if (processedData[0] != ""){
      if (processedData[0] != oldSong){
        oldSong = processedData[0];
        //lcd.clear();
        lcd.setCursor(0, 1);
        lcd.print("                    ");
        //Print the results
        if (processedData[0].length() < 20){
          wherePrint = (20 - (processedData[0].length())) / 2;
          lcd.setCursor(wherePrint, 1);
          lcd.print(processedData[0]);
          //Disable text scrolling
          scrolling = false;
        }else{
          data = processedData[0];
          Li = 20;
          Lii = 0;
          //Enable text scrolling
          scrolling = true;
          
        }
      } 
    }

  }
  //Text scrolling switch
  if (scrolling){
    lcd.print(Scroll_LCD_Left(data));
  }

}