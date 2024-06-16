/*  
--------------------
    Version 1.2
--------------------
Gets song's title and displays it on the 20*4
LCD display. If song's title is smaller than 
21 characters then it is displayed on the
center of the display. Otherwise, the title
scrolls on the second line of the screen. 
Now the lcd turns off when server isn't running
and when spotify isn't runnign time is being
displayed at the middle of the screen.
----------------------------------------------
            Issues:
-Program crashes after 15-20 mins of running
----------------------------------------------
            ToDo:
-W̶h̶e̶n̶ s̶p̶o̶t̶i̶f̶y̶ i̶s̶ n̶o̶t̶ r̶u̶n̶n̶i̶n̶g̶ d̶i̶s̶p̶l̶a̶y̶ day a̶n̶d̶ 
t̶i̶m̶e̶ a̶t̶ t̶h̶e̶ c̶e̶n̶t̶e̶r̶ o̶f̶ t̶h̶e̶ s̶c̶r̶e̶e̶n̶

-M̶a̶k̶e̶ i̶t̶ s̶o̶ i̶t̶ c̶a̶n̶ p̶r̶o̶c̶e̶s̶s̶ m̶u̶l̶t̶i̶p̶l̶e̶ d̶a̶t̶a̶ t̶h̶r̶o̶u̶g̶h̶ 
t̶h̶e̶ s̶e̶r̶i̶a̶l̶ p̶o̶r̶t̶ s̶o̶ i̶t̶ c̶a̶n̶ a̶l̶s̶o̶ r̶e̶a̶d̶ d̶a̶t̶e̶/t̶i̶m̶e̶  
a̶n̶d̶ m̶a̶y̶b̶e̶ a̶r̶t̶i̶s̶t̶ i̶f̶ t̶h̶e̶r̶e̶s̶ s̶p̶a̶c̶e̶ o̶n̶ s̶c̶r̶e̶e̶n̶. 
A̶d̶d̶ a̶ n̶e̶w̶ v̶o̶i̶d̶ w̶h̶i̶c̶h̶ w̶i̶l̶l̶ s̶p̶l̶i̶t̶ t̶h̶e̶ s̶t̶r̶i̶n̶g̶ s̶e̶n̶t̶ 
b̶y̶ t̶h̶e̶ s̶e̶r̶i̶a̶l̶ a̶n̶d̶ s̶p̶l̶i̶t̶ i̶t̶ a̶c̶c̶o̶r̶d̶i̶n̶g̶l̶y̶ t̶o̶ a̶ d̶e̶l̶i̶m̶i̶t̶e̶r̶ 
a̶n̶d̶ t̶h̶e̶n̶ s̶t̶o̶r̶e̶ t̶h̶e̶ d̶a̶t̶a̶ t̶o̶ a̶ g̶l̶o̶b̶a̶l̶ a̶r̶r̶a̶y̶ s̶o̶ t̶h̶e̶y̶ c̶a̶n̶ 
b̶e̶ a̶c̶c̶e̶s̶s̶e̶d̶ f̶o̶r̶ d̶i̶s̶p̶l̶a̶y̶i̶n̶g̶ t̶h̶e̶m̶.
*/


/*            Detailed Description
This code is written in Arduino programming language
and is used to display song and time information on
an LCD screen connected to an Arduino board using the I2C protocol.

The code starts by including the LiquidCrystal_I2C 
and Wire libraries, which provide functions for 
communicating with the LCD screen and for using the 
I2C protocol, respectively. The LiquidCrystal_I2C object
lcd is then defined with the address 0x27 and dimensions 20x4.

Several variables are defined, including Li and Lii,
which are used for scrolling the text on the LCD 
screen, and various String variables for storing
song and time information. The ProcessData function
is defined to take in a String as an argument 
and return an array of two Strings, which represent 
the song and time, respectively. The Scroll_LCD_Left
function is defined to take in a String as an 
argument and return a modified String that is
scrolled on the LCD screen.

In the setup function, the LCD screen is initialized
and the serial port is opened at a baud rate of 9600.
In the main loop function, data is read from a Python 
server over the serial port and stored in the readSong 
variable. If readSong is not empty, the backlight and 
display of the LCD screen are turned on and the data is 
processed using the ProcessData function. The time is
then checked to see if it has changed, and if it has,
it is displayed on the LCD screen. The song is also 
checked to see if it has changed, and if it has, it is
displayed on the LCD screen. If the song is longer 
than 20 characters, it is scrolled on the LCD screen 
using the Scroll_LCD_Left function.

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
String spotify_closed_key = "kyawesgtlu";

String top_l_prefix = "aludsygfwe";
String top_r_prefix = "aisogfhyeq";
String bottm_l_prefix = "wqiyamzdho";
String bottom_r_prefix = "asdfiouywef";
String paused_prefix = "asdgfuaiergwrqc";

int wherePrint;
int time_x = 15;
int time_y = 3;

bool scrolling = false;
bool connected = false;
//Setup lcd display and serial port
void setup() {
  // initializing the LCD.
  lcd.init();  
  // initializing the serial monitor.
  Serial.begin(9600);
}
//Split two different data types
String* ProcessData(String sentData){
  // Declare the songandtime array as a static local variable
  // This will ensure that the array remains valid even after the function returns
  static String songandtime[2];

  String time;
  String song;
  if (sentData.startsWith(delimiter)){
    time = sentData.substring(11, 16);
    song = sentData.substring(16, sentData.length());
    songandtime[0] = song;
    songandtime[1] = time;
  }else{
    songandtime[0] = sentData;
    songandtime[1] = "";
  }
  
  // Return a pointer to the songandtime array
  return songandtime;
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
    //Check If time changed
    if (processedData[1] != ""){
      //if (processedData[1] != oldTime){
      oldTime = processedData[1];

      //lcd.clear();
      lcd.setCursor(0, time_y);
      lcd.print("                    ");

      lcd.setCursor(time_x, time_y);
      //lcd.print(processedData[1]);
      lcd.print(processedData[1]);
      //}
    }
    if (processedData[0] == "ServerExitedByUser"){
      lcd.noBacklight();
      lcd.noDisplay();
      } 
    //Test if song changed
    if (processedData[0] != "" && processedData[0] != "ServerExitedByUser" && processedData[0] != top_l_prefix && processedData[0] != top_r_prefix && processedData[0] != bottm_l_prefix && processedData[0] != bottom_r_prefix && processedData[0] != paused_prefix){
          //Enabling backlight
      lcd.display();
      lcd.backlight();
      if (processedData[0] != oldSong || processedData[0] == spotify_closed_key){
        oldSong = processedData[0];
        if (processedData[0] == spotify_closed_key){ 
          time_x = 7;
          time_y = 1;

          lcd.clear();
          lcd.setCursor(time_x, time_y);
          lcd.print(oldTime);
        }else{
          time_x = 15;
          time_y = 3;

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
  }
  //Text scrolling switch
  if (scrolling){
    lcd.print(Scroll_LCD_Left(data));
  }
}