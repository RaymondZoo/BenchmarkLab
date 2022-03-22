from lib2to3.pgen2.token import RIGHTSHIFT, RIGHTSHIFTEQUAL
from pickletools import read_string1
import random
import serial
import datetime


from tkinter import *
from tkinter import messagebox

#to do:
#control COM, user inputs which com
#control sensordelay and recalibration controls

#backburner:
#maybe add diagram for fun, ehhhhhhhhhhhhhh, idk about this one tbh


#set up frame

root = Tk()
root.title('Flow Loop Testing Interface')
root.resizable(0, 0)
myCanvas = Canvas(root, width = 900, height = 600, bg = "White")
myCanvas.pack()

#logo
fileName = "Benchmark.gif"
pic = PhotoImage(file = fileName)
#resizedPic = pic.subsample(18, 18)

logo = Label(root, image = pic)
logo.photo = pic #ensures label doesn't stay blank
#logo.pack()
logo.place(x = 675, y = 10)
logo.config(width=200, height = 200)

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

#arduino setup 
arduino_port = "COM3"  # serial port of Arduino
baud = 9600  # arduino uno runs at 9600 baud
fileName = "analog-data.csv"  # name of the CSV file generated

ser = serial.Serial(arduino_port, baud)
print("Connected to Arduino port:" + arduino_port)
file = open(fileName, "a")
print("Created file")
global reading
reading = False
global newStart
newStart = True

def play_click(b): #when button clicked
    global reading
    reading = True
        
def pause_click(b): #when button clicked
    global reading
    reading = False

def stop_click(b): #when button clicked
    global reading
    reading = False
    global newStart
    newStart = True
    
def read():
    global reading
    if reading:
        getData = str(ser.readline())
        data = getData[2:-5]

        file = open(fileName, "a")
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

    root.after(1000, read)

my_menu = Menu(root)
root.config(menu=my_menu)

root.after(1000, read)

root.mainloop()


