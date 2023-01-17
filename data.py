gui_counter = 1
on = 1
paused = 1
show_song = 1
top_l = 0
top_r = 0
bottom_r = 1
bottom_l = 0

def on_off():
    global on
    if on == 1:
        on = 0
    else:
        on = 1

def pausing():
    global paused
    if paused == 1:
        paused = 0
    else:
        paused = 1

def showing_song():
    global show_song
    if show_song == 1:
        show_song = 0
    else:
        show_song = 1

def top_left():
    global top_l
    global top_r
    global bottom_r
    global bottom_l
    top_l = 1
    top_r = 0
    bottom_l = 0
    bottom_r = 0

def top_right():
    global top_l
    global top_r
    global bottom_r
    global bottom_l
    top_l = 0
    top_r = 1
    bottom_l = 0
    bottom_r = 0

def bottom_left():
    global top_l
    global top_r
    global bottom_r
    global bottom_l
    top_l = 0
    top_r = 0
    bottom_l = 1
    bottom_r = 0

def bottom_right():
    global top_l
    global top_r
    global bottom_r
    global bottom_l
    top_l = 0
    top_r = 0
    bottom_l = 0
    bottom_r = 1