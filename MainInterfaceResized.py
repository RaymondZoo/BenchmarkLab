import serial
import datetime
import os.path
import AutomaticGraphingProgram as AGP

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from tkinter import *
from tkinter import messagebox

#to do now:

#next:
#backburner:
#maybe add diagram


#set up frame

global root
root = Tk()
root.title('Flow Loop Testing Interface')
root.resizable(False, False)
myCanvas = Canvas(root, width = 1300, height = 1100, bg = "White")
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
Play.place(x = 950, y = 10)

Pause = Button(root, height = 4, width = 28, bg = "yellow", text = "Pause", command=lambda: pause_click(Pause)) #makes button
Pause.pack()
Pause.place(x = 950, y = 120)

Stop = Button(root, height = 4, width = 28, bg = "red", text = "Stop", command=lambda: stop_click(Stop)) #makes button
Stop.pack()
Stop.place(x = 950, y = 230)

newFile = Button(root, height = 4, width = 28, bg  ="light blue", text = "New File", command=lambda: new_File(newFile)) #makes button
newFile.pack()
newFile.place(x = 950, y = 340)

recalibrate = Button(root, height = 4, width = 28, bg  ="violet", text = "Recalibrate", command=lambda: recal(recalibrate)) #makes button
recalibrate.pack()
recalibrate.place(x = 950, y = 450)

newSensorDelay = Button(root, height = 4, width = 28, bg  ="pink", text = "New Sensor Delay", command=lambda: new_sensorDelay(newSensorDelay)) #makes button
newSensorDelay.pack()
newSensorDelay.place(x = 950, y = 560)

newWarningSetup = Button(root, height = 4, width = 28, bg  ="teal", text = "New Warning Setup", command=lambda: new_warningSetup(newWarningSetup)) #makes button
newWarningSetup.pack()
newWarningSetup.place(x = 950, y = 670)

"""
graphButton = Button(root, height = 4, width = 28, bg  ="teal", text = "Graph", command=lambda: drawGraph(graphButton)) #makes button
graphButton.pack()
graphButton.place(x = 675, y = 550)"""

global Autoscrollvar
Autoscrollvar = IntVar()

Autoscroll = Checkbutton(root, height = 2, width = 9, text = "Autoscroll", variable = Autoscrollvar, onvalue = 1, offvalue = 0) #makes button
Autoscroll.place(x = 780, y = 810)

Autoscroll.select()

#log scrollbar

frameScroll = Frame(root)
frameScroll.place(x = 18, y = 70)
frameScroll.config(height = 20, width = 20)
global scroll_bar
scroll_bar = Scrollbar(frameScroll)
global myLog
myLog = Listbox(frameScroll, yscrollcommand = scroll_bar.set,  font = ("Verdana", 15), width= 45, height= 20)
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
#global raw_data
global warningSetup
warningSetup = False
global emailWarning
global paramPLimit

def play_click(b): #when button clicked
    #if COM or file name not set then don't start
    #time.sleep(3)
    global reading
    global conditions
    global root
    if conditions == False: 
        popupwin()
    else:
        global newStart
        global Autoscrollvar
        global scroll_bar
        reading = True
        global myLog
        global file

        if newStart:
            file.write("Time,PressureIn,PressureOut,PressureDifference\n")  
            newStart = False
            myLog.insert(END, "Time,PressureIn,PressureOut,PressureDifference")
            scroll_bar.config(command = myLog.yview)
            if Autoscrollvar.get() == 1:
                myLog.yview(END)

        buttonHelper("START")
        
def pause_click(b): #when button clicked
    global reading
    reading = False

    buttonHelper("PAUSE")

def stop_click(b): #when button clicked
    global reading
    reading = False

    buttonHelper("STOP")
    global newStart
    newStart = True

def new_File(b): #when button clicked
    global reading
    global newFilebool
    if reading == False:
        newFilebool = True
        popupwin()
    else:
        messagebox.showinfo('Warning', 'You must pause or stop the program')

def recal(b): #when button clicked
    global reading
    global conditions
    if conditions == False: 
        popupwin()
    else:
        if reading == False:
            global ser
            ser.write("recalibrate".encode())

            buttonHelper("RECALIBRATE")
            #messagebox.showinfo('Warning', 'Recalibrating may take a moment...')
            #time.sleep(5)
        else:
            messagebox.showinfo('Warning', 'You must pause or stop the program')

def new_sensorDelay(b): #when button clicked
    global reading
    global newSD
    global conditions
    if conditions == False: 
        popupwin()
    else:
        if reading == False:
            newSD = True
            popupwin()
            buttonHelper("NEW SENSOR DELAY")
        else:
            messagebox.showinfo('Warning', 'You must pause or stop the program')

def new_warningSetup(b): #when button clicked
    global reading
    global warningSetup
    global conditions
    if conditions == False: 
        popupwin()
    else:
        if reading == False:
            warningSetup = False
            popupwin()
            buttonHelper("NEW WARNING SETUP")
        else:
            messagebox.showinfo('Warning', 'You must pause or stop the program')

def buttonHelper(string):
    global myLog
    global Autoscrollvar
    global scroll_bar
    global file
    # don't need to open over and over again with open(csvnamed, "a") because this will overwrite
    file.write(str(datetime.datetime.now())+", "+string+" \n") 
    #print(str(datetime.datetime.now())+", "+string+" \n")
    myLog.insert(END, str(datetime.datetime.now())+", "+string+" \n")
    scroll_bar.config(command = myLog.yview)
    if Autoscrollvar.get() == 1:
        myLog.yview(END)


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
    global eName #email entry box
    global pName #pressure limit parameter entry box

    global csvnamed #name of CSV file
    global arduino_port # serial port of Arduino
    global sensorDelay # delay in milliseconds
    global emailWarning #actual email
    global paramPLimit #actual parameter

    global COMset #has the COM been set already or not (because you cannot change the COM once the program has started)
    global newSD #if we have clicked the newSD button
    global newFilebool #if we have clicked the newFile button
    global warningSetup # has the warning system been setup yet

    if COMset == False:
        arduino_port = inputCOM.get()
    if newFilebool == True:
        csvnamed = fName.get()
        Cover = Label(root, bg = "white", width = 75, height = 5)
        Cover.place(x = 0, y = 825)
    if newSD == True:  
        sensorDelay = dName.get()
    if warningSetup == False:
        emailWarning = eName.get()
        paramPLimit = pName.get()
        message = Mail(
            from_email='benchmarklabbot1@gmail.com',
            to_emails = emailWarning,
            subject= csvnamed+' Pressure Warning',
            html_content=' Initialization.' )
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
            warningSetup = True
        except Exception as e:
            emailWarning = ""
            messagebox.showinfo('Warning', 'The email you provided is not valid!')
            print(e) #not sure how this part works

    #this checks that the variable either has a value or isn't needed
    tempbool = (arduino_port != "" or COMset == True)
    tempbool1 = (csvnamed!= ""or newFilebool == False)
    tempbool2 = (sensorDelay != "" or newSD == False)
    tempbool3 = ((emailWarning != "" and paramPLimit != "") or warningSetup == True)

    if tempbool and tempbool1 and tempbool2 and tempbool3:
        
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
        
            if replace == "" or replace == "yes":
                global file
                file = open(fName.get(), "w") # w for new file and a for add to existing file
                print("Created file")
                newFilebool = False
                myLog.delete(0, END) # this line and the one below used to be in newFileButton
                AGP.clear_data()
                global newStart
                newStart = True
            else:
                canCloseBool = False
        

        if canCloseBool == True:
            conditions = True
            top.destroy()
            top.grab_release()


#open the Popup Dialogue
def popupwin():
   #Create a Toplevel window
   global root
   top= Toplevel(root)
   top.geometry("1250x500")

   top.grab_set()
   global COMset
   global newFilebool
   global newSD
   global warningSetup
   
   if COMset == False:
        #Create an Entry Widget in the Toplevel window
        lCOM = Label(top, text="COM Port (ex. \"COM5\" or \"COM3\", check this in Device Manager): ")
        lCOM.place(x = 10, y = 10)
        global inputCOM
        inputCOM = Entry(top, width= 40,  font = ("Verdana", 15))
        inputCOM.place(x = 375, y = 10)
        inputCOM.insert(0, "")

   if newFilebool == True:
        Lfname = Label(top, text="File Name: ")
        Lfname.place(x = 10, y = 50)
        global fName
        fName = Entry(top, width= 40,  font = ("Verdana", 15))
        fName.place(x = 375, y = 50)
        fName.insert(0, str(datetime.datetime.now())[0:10]+"analog-data.csv")

   if newSD == True:
        Delayname = Label(top, text="Sensory Delay in milliseconds: ")
        Delayname.place(x = 10, y = 90)
        global dName
        dName = Entry(top, width= 40,  font = ("Verdana", 15))
        dName.place(x = 375, y = 90)
        dName.insert(0, "1000")

   if warningSetup == False:
        emailName = Label(top, text="Email (for warnings): ")
        emailName.place(x = 10, y = 130)
        global eName
        eName = Entry(top, width= 40,  font = ("Verdana", 15))
        eName.place(x = 375, y = 130)
        
        paramName = Label(top, text="Pressure Limit in psi (for email warnings): ")
        paramName.place(x = 10, y = 170)
        global pName
        pName = Entry(top, width= 40,  font = ("Verdana", 15))
        pName.place(x = 375, y = 170)
        

   #Create a Button Widget in the Toplevel Window
   button= Button(top, text="Ok", command=lambda:close_win(top), width = 10)
   button.place(x = 1100, y = 425)
    
def read():
    global root
    if conditions:
        global reading
        global csvnamed
        global ser
        #global raw_data
        global Autoscrollvar
        global scroll_bar
        global myLog
        #print("check1")
        getData = str(ser.readline())
        data = getData[2:-5]
        if reading:
            global scroll_bar
            global myLog

            # Indices:
            try:
                PressureIN = data[:data.index(",")]
                PressureOUT = data[data.index(",")+1 : data.index(",", data.index(",")+1)]
                PressureDIFF = data[data.index(",", data.index(",")+1)+1:]
            except:
                print("Data line is incomplete: "+data)
            else:
                #send email warning
                if float(PressureDIFF)>float(paramPLimit):
                    message = Mail(
                        from_email='benchmarklabbot1@gmail.com',
                        to_emails = emailWarning,
                        subject= csvnamed + ' Pressure Warning',
                        html_content='The Pressure Limit Parameter is '+paramPLimit+". The Pressure Difference was "+PressureDIFF+". The data line was " +str(datetime.datetime.now())+","+ data )
                    try:
                        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                        response = sg.send(message)
                        print(response.status_code)
                        print(response.body)
                        print(response.headers)
                    except Exception as e:
                        print(e) 

            #graphing data
            raw_data = AGP.read_line_inputs(str(datetime.datetime.now())+","+ data + "\n")
            proc_data = AGP.process_data(raw_data)
            AGP.graph_data(proc_data)
            #AGP.canvas.draw() # do not uncomment this*****

            buttonHelper(data)


    #label for time at the top
    labelTime = Label(root, text = str(datetime.datetime.now())[:-7], font = ("Verdana", 20))
    labelTime.place(x = 175, y = 10)

    #label for filename under the log
    global labelFile
    labelFile = Label(root, text = csvnamed, font = ("Verdana", 20))
    labelFile.place(x = 30, y = 825)
    
    global sensorDelay
    root.grab_set()
    root.after(sensorDelay, read) #sensordelay + needs to match arduino sensor delay

my_menu = Menu(root)
root.config(menu=my_menu)
global csvnamed
csvnamed = ""

root.after(1000, read)

root.mainloop()


