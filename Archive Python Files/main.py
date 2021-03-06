from lib2to3.pgen2.token import RIGHTSHIFT, RIGHTSHIFTEQUAL
from pickletools import read_string1
import random
import serial
import datetime
import time
import os.path

from tkinter import *
from tkinter import messagebox

#to do now:
#control sensordelay and recalibration controls (communication with arduino)
#have to change sensor delay in here too

#next:

#backburner:
#maybe add diagram for fun
#edit exisiting file button, no for now bc idt they need this


#set up frame

root = Tk()
root.title('Flow Loop Testing Interface')
root.resizable(0, 0)
myCanvas = Canvas(root, width = 900, height = 600, bg = "White")
myCanvas.pack()



#commented out right now because PyInstaller doesn't automatically include image dependencies
#we can probably include it later
#icon
"""ico = PhotoImage(file = "mark.gif")
root.iconphoto(True, ico) #doesnt change windows python interpreter icon
#root.iconbitmap(default = "mark.ico") this line is an alternative way but is bad

#logo 
fileName = "Benchmark.gif"
pic = PhotoImage(file = fileName)
resizedPic = pic.subsample(2, 2)

logo = Label(root, image = resizedPic)
logo.photo = resizedPic #ensures label doesn't stay blank
#logo.pack()
logo.place(x = 700, y = 10)
logo.config(width=150, height = 27)"""

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

recalibrate = Button(root, height = 5, width = 28, bg  ="violet", text = "Recalibrate", command=lambda: recal(recalibrate)) #makes button
recalibrate.pack()
recalibrate.place(x = 675, y = 460)


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
global COMset 
COMset = False

def play_click(b): #when button clicked
    #if COM or file name not set then don't start
    global reading
    if conditions == False: 
        popupwin()
    else:
        time.sleep(1)
        global ser
        ser.write("start".encode())
        reading = True
        file.write(str(datetime.datetime.now())+" START \n")  # write data with a newline
        print(str(datetime.datetime.now())+" START \n")
        myLog.insert(END, str(datetime.datetime.now())+" START \n")
        scroll_bar.config(command = myLog.yview)
        if Autoscrollvar.get() == 1:
            myLog.yview(END)

        if newStart:
                file.write("Time,PressureIn,PressureOut,PressureDifference\n")  # write data with a newline
                print("Time,PressureIn,PressureOut,PressureDifference\n")
                newStart = False

                myLog.insert(END, "Time,PressureIn,PressureOut,PressureDifference")
                scroll_bar.config(command = myLog.yview)
                if Autoscrollvar.get() == 1:
                    myLog.yview(END)
    #reading = True
        
def pause_click(b): #when button clicked
    global reading
    reading = False

    global file
    global myLog
    global scroll_bar
    global ser
    ser.write("pause".encode())
    
    file.write(str(datetime.datetime.now())+" PAUSE \n")  # write data with a newline
    print(str(datetime.datetime.now())+" PAUSE \n")
    myLog.insert(END, str(datetime.datetime.now())+" PAUSE \n")
    scroll_bar.config(command = myLog.yview)
    if Autoscrollvar.get() == 1:
        myLog.yview(END)

def stop_click(b): #when button clicked
    global reading
    reading = False
    global ser
    ser.write("stop".encode())
    file.write(str(datetime.datetime.now())+" STOP \n")  # write data with a newline
    print(str(datetime.datetime.now())+" STOP \n")
    myLog.insert(END, str(datetime.datetime.now())+" STOP \n")
    scroll_bar.config(command = myLog.yview)
    if Autoscrollvar.get() == 1:
        myLog.yview(END)
    global newStart
    newStart = True

def new_File(b): #when button clicked
    global reading
    if reading == False:
        popupwin()
    else:
        messagebox.showinfo('Warning', 'You must pause or stop the program')

def recal(b): #when button clicked
    global reading
    if reading == False:
        global ser
        ser.write("recalibrate".encode())
        time.sleep(5)
        file.write(str(datetime.datetime.now())+" RECALIBRATE \n")  # write data with a newline
        print(str(datetime.datetime.now())+" RECALIBRATE \n")
        myLog.insert(END, str(datetime.datetime.now())+" RECALIBRATE \n")
        scroll_bar.config(command = myLog.yview)
        if Autoscrollvar.get() == 1:
            myLog.yview(END)
    else:
        messagebox.showinfo('Warning', 'You must pause or stop the program')

#close the popup window
def close_win(top):
    #arduino setup
    global inputCOM
    global fName
    global csvnamed
    global arduino_port # serial port of Arduino
    global COMset

    arduino_port = ""
    if COMset == True:
        arduino_port = "pass"
    else:
        arduino_port = inputCOM.get()

    if arduino_port != "" and fName.get() !="":
        baud = 9600  # arduino uno runs at 9600 baud
        csvnamed = fName.get()  # name of the CSV file generated
        replace = ""

        
        if os.path.exists(fName.get()):
            replace = messagebox.askquestion('Warning', "\""+fName.get()+"\" already exists. Do you want to replace it?")

        print(replace)

        if replace == "" or replace == "yes":
            if COMset == False:
                global ser
                ser = serial.Serial(arduino_port, baud)
                print("Connected to Arduino port:" + arduino_port)
                COMset = True
            global file
            file = open(fName.get(), "w") # w for new file and a for add to existing file
            print("Created file")

            global conditions
            conditions = True
            top.destroy()
            top.grab_release()
            Cover = Label(root, bg = "white", width = 75, height = 100)
            Cover.place(x = 10, y = 400)
            

#open the Popup Dialogue
def popupwin():
   #Create a Toplevel window
   top= Toplevel(root)
   top.geometry("750x250")

   top.grab_set()
   global COMset
   
   if COMset == False:
    #Create an Entry Widget in the Toplevel window
    lCOM = Label(top, text="COM Port (ex. \"COM5\" or \"COM3\", check this in Device Manager): ")
    lCOM.place(x = 10, y = 10)
    global inputCOM
    inputCOM = Entry(top, width= 25,  font = ("Verdana", 15))
    inputCOM.place(x = 375, y = 10)
    inputCOM.insert(0, "")

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
    global csvnamed
    if reading:
        global ser
        #print("check1")
        getData = str(ser.readline())
        data = getData[2:-5]
        if(data != "Initializing"):
            file = open(csvnamed, "a")
            global newStart
            global scroll_bar
            global myLog
            file.write(str(datetime.datetime.now())+","+ data + "\n")  # write data with a newline
            print(str(datetime.datetime.now())+","+ data + "\n")

            myLog.insert(END, str(datetime.datetime.now())+","+ data)
            scroll_bar.config(command = myLog.yview)
            if Autoscrollvar.get() == 1:
                myLog.yview(END)

    #label for time at the top
    labelTime = Label(root, text = str(datetime.datetime.now())[:-7], font = ("Verdana", 20))
    labelTime.place(x = 100, y = 10)

    #label for filename under the log
    global labelFile
    labelFile = Label(root, text = csvnamed, font = ("Verdana", 20))
    labelFile.place(x = 100, y = 400)
    

    root.after(1000, read) #sensordelay + needs to match arduino sensor delay

my_menu = Menu(root)
root.config(menu=my_menu)

global csvnamed
csvnamed = ""
popupwin()

root.after(1000, read)

root.mainloop()


