"""
---------------------------
        Version 1.0
---------------------------

Send the name of the song to the Arduino board
through port COM6. Plug and play functionality
and displays when song is paused.
---------------------------------------------------------
                Issues:
-When song stopped and started really fast 
arduino displays both paused and the song's name

-Sometimes a crush occures at line 40(tried to
fix it by using try/except, waiting for results)
---------------------------------------------------------
                ToDo:
-Send both time and day/date

-Optimize CPU and RAM usage

-Make it so it mimizes in tray
"""
import serial
from time import strftime
import time
from win32 import win32gui

#----- Variables -----#
connected = 0
old_song = " "
old_time = " "
first_data_transfer = 1
spotify_open = 0
time_prefix = "sgxdfgchjkl"

def get_info_windows():

    windows = []
    paused = "Paused"
    old_window = win32gui.FindWindow("SpotifyMainWindow", None)
    old = win32gui.GetWindowText(old_window)

    def find_spotify_uwp(hwnd, windows):
        text = win32gui.GetWindowText(hwnd)
        try:
            classname = win32gui.GetClassName(hwnd)
        except:
            print("Cant find window")
        if classname == "Chrome_WidgetWin_0" and len(text) > 0:
            windows.append(text)

    if old:
        windows.append(old)
    else:
        win32gui.EnumWindows(find_spotify_uwp, windows)

    # If Spotify isn't running the list will be empty
    if len(windows) == 0:
        return " ", " "

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

def artist():
    return get_info_windows()[1]


def song():
    return get_info_windows()[0]

# def TimeNDate():
#     global time_prefix
#     global arduino
#     global old_time
#     time = strftime('%H:%M %p')
    
#     if time != old_time:
#         old_time = time
#         data = time_prefix + old_time + time_prefix
#         print(data)
#         arduino.write(data.encode())

def connect():
    global arduino
    global connected
    try:
        arduino = serial.Serial('com6', 9600)
        connected = 1
        print("Connected")
        print(arduino)
    except:
        connected = 0

def getSong():
    global arduino
    global old_song
    global first_data_transfer

    current_song = song()
    current_artist = artist()
    data = [current_song, current_artist]
    if current_song != old_song:
        try:
            arduino.write(current_song.encode())
            print(current_song)
            old_song = current_song

        except:
            print("Board Disconnected")
            connect()
            while True:
                if connected == 0:
                    connect()
                else:
                    first_data_transfer = 1
                    break
def main():
    global first_data_transfer
    global arduino
    while True:
        if connected == 0:
            connect()
            first_data_transfer = 1
        else:
            if first_data_transfer == 1:
                time.sleep(4)
                # TimeNDate()
                getSong()
                first_data_transfer = 0
            else:
                # TimeNDate()
                getSong()

main()