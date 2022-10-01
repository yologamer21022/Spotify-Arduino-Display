"""
---------------------------
        Version 1.2
---------------------------

Send the name of the song to the Arduino board
through port COM6. Plug and play functionality
and displays when song is paused. Now shows and
the time at the bottom corner and when the exe
is running at the background a small icon shows
at the system tray from where you can close the
executable. I've added some things but i can't 
remember. The program is now better and faster.
---------------------------------------------------------
                Issues:
-At this point i have lost any form of sanity while
editing this at 2:40 am during a cold Friday night
suffering from mild covid symptoms. If anyone ever
gets to see this program please excuse me for my bad
problem solving method my 16 year old self followed to
make this one project.

-When song stopped and started really fast 
arduino displays both paused and the song's name

-S̶o̶m̶e̶t̶i̶m̶e̶s̶ a̶ c̶r̶u̶s̶h̶ o̶c̶c̶u̶r̶e̶s̶ a̶t̶ l̶i̶n̶e̶ 4̶0̶
(̶t̶r̶i̶e̶d̶ t̶o̶ f̶i̶x̶ i̶t̶ b̶y̶ u̶s̶i̶n̶g̶ t̶r̶y̶/e̶x̶c̶e̶p̶t̶, w̶a̶i̶t̶i̶n̶g̶ f̶o̶r̶ r̶e̶s̶u̶l̶t̶s̶)̶
---------------------------------------------------------
                ToDo:
-S̶e̶n̶d̶ b̶o̶t̶h̶ s̶o̶n̶g̶ a̶n̶d̶ t̶i̶m̶e̶ a̶s̶ a̶n̶ a̶r̶r̶a̶y̶ t̶o̶ a̶v̶o̶i̶d̶
 c̶r̶a̶s̶h̶e̶s̶ w̶h̶e̶n̶ p̶r̶o̶g̶r̶a̶m̶ t̶r̶i̶e̶s̶ t̶o̶ s̶e̶n̶d̶ b̶o̶t̶h̶ a̶t̶ t̶h̶e̶
s̶a̶m̶e̶ t̶i̶m̶e̶.
(Tried to but i might have fixed it otherwise)

-W̶h̶e̶n̶ s̶p̶o̶t̶i̶f̶y̶ i̶s̶ n̶o̶t̶ r̶u̶n̶n̶i̶n̶g̶ d̶i̶s̶p̶l̶a̶y̶ d̶a̶y̶ a̶n̶d̶ 
 t̶i̶m̶e̶ a̶t̶ t̶h̶e̶ c̶e̶n̶t̶e̶r̶ o̶f̶ t̶h̶e̶ s̶c̶r̶e̶e̶n̶

-S̶e̶n̶d̶ b̶o̶t̶h̶ t̶i̶m̶e̶ and day/date

-O̶p̶t̶i̶m̶i̶z̶e̶ C̶P̶U̶ a̶n̶d̶ R̶A̶M̶ u̶s̶a̶g̶e̶ 

-M̶a̶k̶e̶ i̶t̶ s̶o̶ i̶t̶ m̶i̶m̶i̶z̶e̶s̶ i̶n̶ t̶r̶a̶y̶

-F̶i̶x̶ g̶e̶t̶_̶i̶n̶f̶o̶_̶w̶i̶n̶d̶o̶w̶s̶(̶)̶ e̶r̶r̶o̶r̶
"""

import serial
import time
import win32gui
import atexit
import pkg_resources
from infi.systray import SysTrayIcon

#----- Variables -----#
connected = 0
old_song = " "
old_time = " "
first_data_transfer = 1
spotify_open = 0
time_prefix = "sgxdfgchjkl"
exit_by_user = 0
spotify_closed_key = "kyawesgtlu"
#           Exit Handler
#-----------------------------------
def exit_handler():
    global arduino
    arduino.write("ServerExitedByUser".encode())
#-----------------------------------
#           SysTray
#-----------------------------------
def on_quit_callback(systray):
    global exit_by_user
    exit_by_user = 1
def say_hello(systray):
    print("hi")
menu_options = (("Thanks For Trusting Us", None, say_hello),)
systray = SysTrayIcon("icon.ico", "Arduino Spotify Checker",menu_options, on_quit=on_quit_callback)
systray.start()
#-----------------------------------
#Get Spotify Window Info
def get_info_windows():
    windows = []
    paused = "Paused"
    old_window = win32gui.FindWindow("SpotifyMainWindow", None)
    old = win32gui.GetWindowText(old_window)

    def find_spotify_uwp(hwnd, windows):
        text = win32gui.GetWindowText(hwnd)
        try:
            classname = win32gui.GetClassName(hwnd)
            if classname == "Chrome_WidgetWin_0" and len(text) > 0:
                windows.append(text)
        except:
            print("Cant find window")
    if old:
        windows.append(old)
    else:
        win32gui.EnumWindows(find_spotify_uwp, windows)
    # If Spotify isn't running the list will be empty
    if len(windows) == 0:
        return spotify_closed_key, spotify_closed_key
    # Local songs may only have a title field
    try:
        artist, track = windows[0].split(" - ", 1)
    except ValueError:
        artist = ""
        track = windows[0]
    # The window title is the default one when paused
    if windows[0].startswith("Spotify"):
        return paused, paused

    return track, artist

#Split get_info_windows() result
#-----------------------------------
def artist():
    return get_info_windows()[1]
def song():
    return get_info_windows()[0]
#-----------------------------------
#Connect With the Arduino via Com6 port
def connect():
    #Set Global Variables
    global arduino
    global connected
    try:
        arduino = serial.Serial('com6', 9600)
        print("Connected")
        print(arduino)
        connected = 1
    except:
        connected = 0

#Send time and date data
#-----------------------------------
def TimeNDate():
    #Set Global Variables
    global time_prefix
    global arduino
    global old_time
    global first_data_transfer

    t = time.localtime()
    current_time = time.strftime("%H:%M", t) #Get Current Time
    
    if current_time != old_time:        #Send Time When A Minute Passes
        try:
            old_time = current_time
            data = time_prefix + old_time
            print(data)
            arduino.write(data.encode())
        except:
            #It means board is disconnected
            print("Board Disconnected")
            connect()
 
#-----------------------------------

#Get Song's title and send it to arduino
def getSong():
    #Set Global Variables
    global arduino
    global old_song
    global first_data_transfer
    global exit_by_user

    current_song = song()
    current_artist = artist()
    data = [current_song, current_artist]
    if current_song != old_song:
        try:
            #If it can't send the data
            arduino.write(current_song.encode())
            print(current_song)
            old_song = current_song

        except:
            #It means board is disconnected
            print("Board Disconnected")
            connect()
            while True:
                #Close Program When Terminated By Ststem Tray
                time.sleep(0.2)
                if exit_by_user == 1:
                    break
                if connected == 0:
                    connect()
                else:
                    first_data_transfer = 1
                    break
#Main def
#----------------------------------------------------------------------
def main():
    #Set Global Variables
    global first_data_transfer
    global arduino
    global exit_by_user

    while True:
        #Close Program When Terminated By Ststem Tray
        if exit_by_user == 1:
            break
        #DO the magic stuff
        if connected == 0:
            connect()
            first_data_transfer = 1
        else:
            if first_data_transfer == 1:
                time.sleep(4)
                TimeNDate()
                time.sleep(0.2)                                     #Performance Fix?
                getSong()
                first_data_transfer = 0
            else:
                TimeNDate()
                time.sleep(0.2)                                     #Performance Fix?
                getSong()
#----------------------------------------------------------------------
#Asighn what to do when program exits
atexit.register(exit_handler)
#Start the main function
main()