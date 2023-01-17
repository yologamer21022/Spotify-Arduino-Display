import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
import data
on = data.on
paused = data.paused
show_song = data.show_song
class App:
    global on
    global paused
    global show_song
    def __init__(self, root):
        #setting title
        root.title("Python-Arduino Clock")
        root.configure(background='#dedad9')
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLabel_285=tk.Label(root)
        GLabel_285["bg"] = "#e3e3e3"
        ft = tkFont.Font(family='Times',size=14)
        GLabel_285["font"] = ft
        GLabel_285["fg"] = "#333333"
        GLabel_285["justify"] = "center"
        GLabel_285["text"] = "Python Arduino Clock"
        GLabel_285["relief"] = "ridge"
        GLabel_285.place(x=-1,y=-1,width=601,height=56)

        GCheckBox_403=tk.Checkbutton(root)
        GCheckBox_403["bg"] = "#d0cbcb"
        ft = tkFont.Font(family='Times',size=14)
        GCheckBox_403["font"] = ft
        GCheckBox_403["fg"] = "#333333"
        GCheckBox_403["justify"] = "center"
        GCheckBox_403["text"] = "On/Off"
        GCheckBox_403.place(x=30,y=80,width=134,height=79)
        if on == 0:
            GCheckBox_403["offvalue"] = "0"
            GCheckBox_403["onvalue"] = "1"
        else:
            GCheckBox_403["offvalue"] = "1"
            GCheckBox_403["onvalue"] = "0"      
        GCheckBox_403["command"] = self.GCheckBox_403_command

        GCheckBox_192=tk.Checkbutton(root)
        GCheckBox_192["bg"] = "#d0cbcb"
        ft = tkFont.Font(family='Times',size=14)
        GCheckBox_192["font"] = ft
        GCheckBox_192["fg"] = "#333333"
        GCheckBox_192["justify"] = "center"
        GCheckBox_192["text"] = "Paused"
        GCheckBox_192.place(x=230,y=80,width=134,height=79)
        if paused == 0:
            GCheckBox_192["offvalue"] = "0"
            GCheckBox_192["onvalue"] = "1"
        else:
            GCheckBox_192["offvalue"] = "1"
            GCheckBox_192["onvalue"] = "0"           
        GCheckBox_192["command"] = self.GCheckBox_192_command

        GCheckBox_426=tk.Checkbutton(root)
        GCheckBox_426["bg"] = "#d0cbcb"
        ft = tkFont.Font(family='Times',size=14)
        GCheckBox_426["font"] = ft
        GCheckBox_426["fg"] = "#333333"
        GCheckBox_426["justify"] = "center"
        GCheckBox_426["text"] = "Show Song"
        GCheckBox_426.place(x=420,y=80,width=134,height=79)
        if show_song == 0:
            GCheckBox_426["offvalue"] = "0"
            GCheckBox_426["onvalue"] = "1"
        else:
            GCheckBox_426["offvalue"] = "1"
            GCheckBox_426["onvalue"] = "0"
        GCheckBox_426["command"] = self.GCheckBox_426_command
        #GCheckBox_426.select()

        GLabel_149=tk.Label(root)
        GLabel_149["bg"] = "#e3e3e3"
        ft = tkFont.Font(family='Times',size=16)
        GLabel_149["font"] = ft
        GLabel_149["fg"] = "#333333"
        GLabel_149["justify"] = "center"
        GLabel_149["text"] = "Time Position"
        GLabel_149.place(x=180,y=240,width=238,height=45)

        GButton_684=tk.Button(root)
        GButton_684["bg"] = "#ddc0c0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_684["font"] = ft
        GButton_684["fg"] = "#000000"
        GButton_684["justify"] = "center"
        GButton_684["text"] = "Top L"
        GButton_684.place(x=70,y=320,width=115,height=55)
        GButton_684["command"] = self.GButton_684_command

        GButton_433=tk.Button(root)
        GButton_433["bg"] = "#ddc0c0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_433["font"] = ft
        GButton_433["fg"] = "#000000"
        GButton_433["justify"] = "center"
        GButton_433["text"] = "Bottom L"
        GButton_433.place(x=70,y=410,width=115,height=55)
        GButton_433["command"] = self.GButton_433_command

        GButton_245=tk.Button(root)
        GButton_245["bg"] = "#ddc0c0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_245["font"] = ft
        GButton_245["fg"] = "#000000"
        GButton_245["justify"] = "center"
        GButton_245["text"] = "Top R"
        GButton_245.place(x=400,y=320,width=115,height=55)
        GButton_245["command"] = self.GButton_245_command

        GButton_764=tk.Button(root)
        GButton_764["bg"] = "#ddc0c0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_764["font"] = ft
        GButton_764["fg"] = "#000000"
        GButton_764["justify"] = "center"
        GButton_764["text"] = "Bottom R"
        GButton_764.place(x=400,y=410,width=115,height=55)
        GButton_764["command"] = self.GButton_764_command

    def GCheckBox_403_command(self):
        data.on_off()


    def GCheckBox_192_command(self):
        data.pausing()


    def GCheckBox_426_command(self):
        data.showing_song()


    def GButton_684_command(self):
        data.top_left()


    def GButton_433_command(self):
        data.bottom_left()


    def GButton_245_command(self):
        data.top_right()


    def GButton_764_command(self):
        data.bottom_right()



def on_closing():
    global on
    global paused
    global show_song
    if messagebox.askokcancel("Quit", "Do you want to exit settings?"):
        root.destroy()  
        data.gui_counter = 1
        on = data.on
        paused = data.paused
        show_song = data.show_song

def initiate_GUI():
    global root
    root = tk.Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()



