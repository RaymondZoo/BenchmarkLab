from asyncio.windows_events import NULL
from email.contentmanager import raw_data_manager
from lib2to3.pgen2.token import RIGHTSHIFT, RIGHTSHIFTEQUAL
from pickletools import read_string1
import random
import serial
import datetime
import time
import os.path
import AutomaticGraphingProgram as AGP

from tkinter import *
from tkinter import messagebox

#to do now:

#next:
#backburner:
#maybe add diagram for fun
#edit exisiting file button, no for now bc idt they need this


#set up frame

global root
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
Play = Button(root, height = 4, width = 28, bg = "green", text = "Play", command=lambda: play_click(Play)) #makes button
Play.pack()
Play.place(x = 675, y = 10)

Pause = Button(root, height = 4, width = 28, bg = "yellow", text = "Pause", command=lambda: pause_click(Pause)) #makes button
Pause.pack()
Pause.place(x = 675, y = 100)

Stop = Button(root, height = 4, width = 28, bg = "red", text = "Stop", command=lambda: stop_click(Stop)) #makes button
Stop.pack()
Stop.place(x = 675, y = 190)

newFile = Button(root, height = 4, width = 28, bg  ="light blue", text = "New File", command=lambda: new_File(newFile)) #makes button
newFile.pack()
newFile.place(x = 675, y = 280)

recalibrate = Button(root, height = 4, width = 28, bg  ="violet", text = "Recalibrate", command=lambda: recal(recalibrate)) #makes button
recalibrate.pack()
recalibrate.place(x = 675, y = 370)

newSensorDelay = Button(root, height = 4, width = 28, bg  ="pink", text = "New Sensor Delay", command=lambda: new_sensorDelay(newSensorDelay)) #makes button
newSensorDelay.pack()
newSensorDelay.place(x = 675, y = 460)

"""
graphButton = Button(root, height = 4, width = 28, bg  ="teal", text = "Graph", command=lambda: drawGraph(graphButton)) #makes button
graphButton.pack()
graphButton.place(x = 675, y = 550)"""

global Autoscrollvar
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
global sensorDelay
sensorDelay = 1000
global newFilebool
newFilebool = True
global newSD
newSD = True
global raw_data

def play_click(b): #when button clicked
    #if COM or file name not set then don't start
    #time.sleep(3)
    global reading
    global conditions
    global root
    if conditions == False: 
        popupwin()
    else:
        global ser
        global newStart
        global csvnamed
        global Autoscrollvar
        global scroll_bar
        reading = True
        global myLog

        file = open(csvnamed, "a")

        if newStart:
            file.write("Time,PressureIn,PressureOut,PressureDifference\n")  # write data with a newline
            print("Time,PressureIn,PressureOut,PressureDifference\n")
            newStart = False
            myLog.insert(END, "Time,PressureIn,PressureOut,PressureDifference")
            scroll_bar.config(command = myLog.yview)
            if Autoscrollvar.get() == 1:
                myLog.yview(END)

        file.write(str(datetime.datetime.now())+", START \n")  # write data with a newline
        print(str(datetime.datetime.now())+", START \n")
        myLog.insert(END, str(datetime.datetime.now())+", START \n")
        scroll_bar.config(command = myLog.yview)
        if Autoscrollvar.get() == 1:
            myLog.yview(END)
        
        
    #reading = True
        
def pause_click(b): #when button clicked
    global reading
    reading = False
    global ser
    global csvnamed
    global myLog
    global Autoscrollvar
    global scroll_bar
    global root

    file = open(csvnamed, "a") #was probably being weird before b/c I referenced the global file variable each time, maybe opening the same file twice which meant the "PAUSE" was sent way later

    file.write(str(datetime.datetime.now())+", PAUSE \n")
    print(str(datetime.datetime.now())+", PAUSE \n")
    myLog.insert(END, str(datetime.datetime.now())+", PAUSE \n")
    scroll_bar.config(command = myLog.yview)  
    if Autoscrollvar.get() == 1:
        myLog.yview(END)

def stop_click(b): #when button clicked
    global root
    global reading
    reading = False
    global ser

    global csvnamed

    global Autoscrollvar
    global scroll_bar
    global myLog

    file = open(csvnamed, "a")

    file.write(str(datetime.datetime.now())+", STOP \n")  # write data with a newline
    print(str(datetime.datetime.now())+", STOP \n")
    myLog.insert(END, str(datetime.datetime.now())+", STOP \n")
    scroll_bar.config(command = myLog.yview)
    if Autoscrollvar.get() == 1:
        myLog.yview(END)
    global newStart
    newStart = True

def new_File(b): #when button clicked
    global root
    global reading
    global newFilebool
    global myLog
    if reading == False:
        newFilebool = True
        popupwin()
        global myLog
        myLog.delete(0, END)
    else:
        messagebox.showinfo('Warning', 'You must pause or stop the program')

def recal(b): #when button clicked
    global root
    global reading
    global conditions
    global Autoscrollvar
    global scroll_bar
    global myLog
    if conditions == False: 
        popupwin()
    else:
        if reading == False:
            global ser
            ser.write("recalibrate".encode())

            global csvnamed 

            file = open(csvnamed, "a") 
            file.write(str(datetime.datetime.now())+", RECALIBRATE \n")  # write data with a newline
            print(str(datetime.datetime.now())+", RECALIBRATE \n")
            myLog.insert(END, str(datetime.datetime.now())+", RECALIBRATE \n")
            scroll_bar.config(command = myLog.yview)
            if Autoscrollvar.get() == 1:
                myLog.yview(END)
            #messagebox.showinfo('Warning', 'Recalibrating may take a moment...')
            #time.sleep(5)
        else:
            messagebox.showinfo('Warning', 'You must pause or stop the program')

def new_sensorDelay(b): #when button clicked
    global reading
    global root
    global newSD
    global conditions
    global Autoscrollvar
    global scroll_bar
    global myLog
    if conditions == False: 
        popupwin()
    else:
        if reading == False:
            newSD = True
            popupwin()
            file = open(csvnamed, "a") 
            file.write(str(datetime.datetime.now())+", NEW SENSOR DELAY \n")  # write data with a newline
            print(str(datetime.datetime.now())+", NEW SENSOR DELAY \n")
            myLog.insert(END, str(datetime.datetime.now())+", NEW SENSOR DELAY \n")
            scroll_bar.config(command = myLog.yview)
            if Autoscrollvar.get() == 1:
                myLog.yview(END)
        else:
            messagebox.showinfo('Warning', 'You must pause or stop the program')


#def drawGraph(b): #when button clicked
    """
    global reading
    global raw_data
    if(reading == False):
        proc_data = AGP.process_data(raw_data)
        AGP.graph_data(proc_data)
    """
    """
    global root
    global top
    top = Toplevel(root)
    top.geometry("750x250")
    top.grab_set()
    top.grab_set()"""
    """
    #LGraph = Label(top, text="Time Interval (For raw data, input 0): ")
    #LGraph.place(x = 10, y = 10)
    #global inputGraph
    #inputGraph = Entry(top, width= 25,  font = ("Verdana", 15))
    #inputGraph.place(x = 375, y = 10)
    #inputGraph.insert(0, "")

    """
    """
     #Create a Button Widget in the Toplevel Window
     button= Button(top, text="Ok", command=lambda:closeGraphSetup(top), width = 5)
     button.place(x = 660, y = 140)
    
def closeGraphSetup(top):
    top.destroy()
    top.grab_release()
    return"""

#close the popup window
def close_win(top):
    #arduino setup
    global root

    global conditions#whether everything has been met or not for read() to work

    global inputCOM #COM entry box
    global fName #fileName entry box
    global dName #sensor delay entry box

    global csvnamed #name of CSV file
    global arduino_port # serial port of Arduino
    global sensorDelay # delay in milliseconds

    global COMset #has the COM been set already or not (because you cannot change the COM once the program has started)
    global newSD #if we have clicked the newSD button
    global newFilebool #if we have clicked the newFile button

    if COMset == False:
        arduino_port = inputCOM.get()
    if newFilebool == True:
        csvnamed = fName.get()
    if newSD == True:  
        sensorDelay = dName.get()

    if (arduino_port != "" or COMset == True) and (csvnamed!= ""or newFilebool == False) and (sensorDelay != "" or newSD == False):
        baud = 9600  # arduino uno runs at 9600 baud
        replace = ""
        canCloseBool = True

        if COMset == False:
                global ser
                ser = serial.Serial(arduino_port, baud)
                print("Connected to Arduino port:" + arduino_port)
                COMset = True
        if newSD == True:
            ser.write(("sd "+str(sensorDelay)).encode())
            newSD = False
        if newFilebool == True:
            if os.path.exists(fName.get()):
                replace = messagebox.askquestion('Warning', "\""+fName.get()+"\" already exists. Do you want to replace it?")

            #print(replace)
            if replace == "" or replace == "yes":
                global file
                file = open(fName.get(), "w") # w for new file and a for add to existing file
                print("Created file")
                newFilebool = False
            else:
                canCloseBool = False

        if canCloseBool == True:
            conditions = True
            top.destroy()
            top.grab_release()
            Cover = Label(root, bg = "white", width = 75, height = 100)
            Cover.place(x = 10, y = 400)


            

#open the Popup Dialogue
def popupwin():
   #Create a Toplevel window
   global root
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

   if newFilebool == True:
        Lfname = Label(top, text="File Name: ")
        Lfname.place(x = 10, y = 50)
        global fName
        fName = Entry(top, width= 25,  font = ("Verdana", 15))
        fName.place(x = 375, y = 50)
        fName.insert(0, str(datetime.datetime.now())[0:10]+"analog-data.csv")

   if newSD == True:
        Delayname = Label(top, text="Sensory Delay in milliseconds: ")
        Delayname.place(x = 10, y = 90)
        global dName
        dName = Entry(top, width= 25,  font = ("Verdana", 15))
        dName.place(x = 375, y = 90)
        dName.insert(0, "1000")

   

   #Create a Button Widget in the Toplevel Window
   button= Button(top, text="Ok", command=lambda:close_win(top), width = 5)
   button.place(x = 660, y = 140)
    
def read():
    global root
    if conditions:
        global reading
        global csvnamed
        global ser
        global raw_data
        global Autoscrollvar
        global scroll_bar
        global myLog
        #print("check1")
        getData = str(ser.readline())
        data = getData[2:-5]
        if reading:
            file = open(csvnamed, "a")
            global scroll_bar
            global myLog
            file.write(str(datetime.datetime.now())+","+ data + "\n")  # write data with a newline
            print(str(datetime.datetime.now())+","+ data + "\n")

            raw_data = AGP.read_line_inputs(str(datetime.datetime.now())+","+ data + "\n")
            proc_data = AGP.process_data(raw_data)
            AGP.graph_data(proc_data)

            myLog.insert(END, str(datetime.datetime.now())+","+ data)
            scroll_bar.config(command = myLog.yview)
            if Autoscrollvar.get() == 1:
                myLog.yview(END)
                #myLog.see(END)


    #label for time at the top
    labelTime = Label(root, text = str(datetime.datetime.now())[:-7], font = ("Verdana", 20))
    labelTime.place(x = 100, y = 10)

    #label for filename under the log
    global labelFile
    labelFile = Label(root, text = csvnamed, font = ("Verdana", 20))
    labelFile.place(x = 100, y = 400)
    
    global sensorDelay
    root.grab_set()
    root.after(sensorDelay, read) #sensordelay + needs to match arduino sensor delay

my_menu = Menu(root)
root.config(menu=my_menu)
global csvnamed
csvnamed = ""
#popupwin()

root.after(1000, read)

root.mainloop()


