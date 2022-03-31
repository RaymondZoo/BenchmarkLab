from lib2to3.pgen2.token import RIGHTSHIFT, RIGHTSHIFTEQUAL
from pickletools import read_string1
import random
import serial
import datetime
import os.path

from tkinter import *
from tkinter import messagebox

#to do now:
#user inputs which COM
#new file button, user inputs file name, current file name label

#next:
#control sensordelay and recalibration controls (communication with arduino)
#have to change sensor delay in here too


#backburner:
#maybe add diagram for fun, ehhhhhhhhhhhhhh, idk about this one tbh
#edit exisiting file button, no for now bc idt they need this


#set up frame

root = Tk()
root.title('Flow Loop Testing Interface')
root.resizable(0, 0)
myCanvas = Canvas(root, width = 900, height = 600, bg = "White")
myCanvas.pack()

#icon
ico = PhotoImage(file = "mark.gif")
root.iconphoto(True, ico) #doesnt change windows python interpreter icon
#root.iconbitmap(default = "mark.ico")

#logo
fileName = "Benchmark.gif"
pic = PhotoImage(file = fileName)
resizedPic = pic.subsample(2, 2)

logo = Label(root, image = resizedPic)
logo.photo = resizedPic #ensures label doesn't stay blank
#logo.pack()
logo.place(x = 700, y = 10)
logo.config(width=150, height = 27)

#buttons
Play = Button(root, height = 5, width = 28, bg = "green", text = "Play", command=lambda: play_click(Play)) #makes button
Play.pack()
Play.place(x = 675, y = 100)

Pause = Button(root, height = 5, width = 28, bg = "yellow", text = "Pause", command=lambda: pause_click(Pause)) #makes button
Pause.pack()
Pause.place(x = 675, y = 190)

Stop = Button(root, height = 5, width = 28, bg = "red", text = "Stop", command=lambda: stop_click(Stop)) #makes button
Stop.pack()
Stop.place(x = 675, y = 280)

newFile = Button(root, height = 5, width = 28, bg  ="light blue", text = "New File", command=lambda: new_File(newFile)) #makes button
newFile.pack()
newFile.place(x = 675, y = 370)

Autoscrollvar = IntVar()

Autoscroll = Checkbutton(root, height = 2, width = 10, text = "Autoscroll", variable = Autoscrollvar, onvalue = 1, offvalue = 0) #makes button
Autoscroll.place(x = 530, y = 325)

Autoscroll.select()

#log scrollbar

frameScroll = Frame(root)
frameScroll.place(x = 18, y = 60)
frameScroll.config(height = 10, width = 10)
global scroll_bar
scroll_bar = Scrollbar(frameScroll)
global myLog
myLog = Listbox(frameScroll, yscrollcommand = scroll_bar.set,  font = ("Verdana", 15), width= 45, height= 10)
myLog.pack( side = LEFT, fill = BOTH, expand= True )
scroll_bar.pack( side = RIGHT, fill = Y, expand= True)
#myLog.place(x = 0, y= 0)
scroll_bar.config(command = myLog.yview)

global reading
reading = False
global newStart
newStart = True
global conditions
conditions = False

def play_click(b): #when button clicked
    #if COM or file name not set then don't start
    global reading
    if conditions == False: 
        popupwin()
    else:
        reading = True
    #reading = True
        
def pause_click(b): #when button clicked
    global reading
    reading = False

def stop_click(b): #when button clicked
    global reading
    reading = False
    global newStart
    newStart = True

def new_File(b): #when button clicked
    global reading
    if reading == False:
        popupwin()
    else:
        messagebox.showinfo('Warning', 'You must pause or stop the program')

#close the popup window
def close_win(top):
    #arduino setup
    global inputCOM
    global fName
    global csvnamed
    global arduino_port
    if inputCOM.get() != "" or fName.get() !="": 
        arduino_port = inputCOM.get()  # serial port of Arduino
        baud = 9600  # arduino uno runs at 9600 baud
        csvnamed = fName.get()  # name of the CSV file generated
        replace = ""

        
        if os.path.exists(fName.get()):
            replace = messagebox.askquestion('Warning', "\""+fName.get()+"\" already exists. Do you want to replace it?")

        print(replace)

        if replace == "" or replace == "yes":
            global ser
            ser = serial.Serial(arduino_port, baud)
            print("Connected to Arduino port:" + arduino_port)
            global file
            file = open(fName.get(), "w") # w for new file and a for add to existing file
            print("Created file")

            global conditions
            conditions = True
            top.destroy()
            top.grab_release()

#open the Popup Dialogue
def popupwin():
   #Create a Toplevel window

   top= Toplevel(root)
   top.geometry("750x250")

   top.grab_set()

   #Create an Entry Widget in the Toplevel window
   lCOM = Label(top, text="COM Port (ex. \"COM5\" or \"COM3\", check this in Device Manager): ")
   lCOM.place(x = 10, y = 10)
   global inputCOM
   inputCOM = Entry(top, width= 25,  font = ("Verdana", 15))
   inputCOM.place(x = 375, y = 10)

   Lfname = Label(top, text="File Name: ")
   Lfname.place(x = 10, y = 50)
   global fName
   fName = Entry(top, width= 25,  font = ("Verdana", 15))
   fName.place(x = 375, y = 50)
   fName.insert(0, str(datetime.datetime.now())[0:10]+"analog-data.csv")

   

   #Create a Button Widget in the Toplevel Window
   button= Button(top, text="Ok", command=lambda:close_win(top), width = 5)
   button.place(x = 660, y = 100)
    
def read():
    global reading
    if reading:
        global ser
        getData = str(ser.readline())
        data = getData[2:-5]

        global csvnamed
        
        file = open(csvnamed, "a")
        global newStart
        global scroll_bar
        global myLog
        if newStart:
            file.write("Time,PressureIn,PressureOut,PressureDifference\n")  # write data with a newline
            print("Time,PressureIn,PressureOut,PressureDifference\n")
            newStart = False

            myLog.insert(END, "Time,PressureIn,PressureOut,PressureDifference")
            scroll_bar.config(command = myLog.yview)
            if Autoscrollvar.get() == 1:
                myLog.yview(END)
        else:
            file.write(str(datetime.datetime.now())+","+ data + "\n")  # write data with a newline
            print(str(datetime.datetime.now())+","+ data + "\n")

            myLog.insert(END, str(datetime.datetime.now())+","+ data)
            scroll_bar.config(command = myLog.yview)
            if Autoscrollvar.get() == 1:
                myLog.yview(END)

    labelTime = Label(root, text = str(datetime.datetime.now())[:-7], font = ("Verdana", 20))
    labelTime.place(x = 100, y = 10)

    root.after(1000, read) #sensordelay

my_menu = Menu(root)
root.config(menu=my_menu)

popupwin()

root.after(1000, read)

root.mainloop()


