import serial
import datetime
import time
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
#myCanvas = Canvas(root, width = 1300, height = 1100, bg = "White")
root.geometry("1700x1200")


#buttons, original size was "height = 4, width = 28,"
Play = Button(root,  bg = "green", text = "Play", command=lambda: play_click(Play)) #makes button
#Play.pack()
#Play.place(x = 950, y = 10)

Pause = Button(root, bg = "yellow", text = "Pause", command=lambda: pause_click(Pause)) #makes button
#Pause.pack()
#Pause.place(x = 950, y = 120)

Stop = Button(root, bg = "red", text = "Stop", command=lambda: stop_click(Stop)) #makes button
#Stop.pack()
#Stop.place(x = 950, y = 230)

newFile = Button(root, bg = "light blue", text = "New File", command=lambda: new_File(newFile)) #makes button
#newFile.pack()
#newFile.place(x = 950, y = 340)

recalibrate = Button(root, bg = "violet", text = "Recalibrate", command=lambda: recal(recalibrate)) #makes button
#recalibrate.pack()
#recalibrate.place(x = 950, y = 450)

newSensorDelay = Button(root, bg = "pink", text = "New Sensor Delay", command=lambda: new_sensorDelay(newSensorDelay)) #makes button
#newSensorDelay.pack()
#newSensorDelay.place(x = 950, y = 560)

newWarningSetup = Button(root, bg = "teal", text = "New Warning Setup", command=lambda: new_warningSetup(newWarningSetup)) #makes button
#newWarningSetup.pack()
#newWarningSetup.place(x = 950, y = 670)

newTransducer = Button(root, bg = "orange", text = "New Transducer", command=lambda: new_transducer(newTransducer)) #makes button
#newTransducer.pack()
#newTransducer.place(x = 950, y = 780)

"""
graphButton = Button(root, height = 4, width = 28, bg  ="teal", text = "Graph", command=lambda: drawGraph(graphButton)) #makes button
graphButton.pack()
graphButton.place(x = 675, y = 550)"""

global Autoscrollvar
Autoscrollvar = IntVar()

Autoscroll = Checkbutton(root, text = "Autoscroll", variable = Autoscrollvar, onvalue = 1, offvalue = 0) #makes button
#Autoscroll.place(x = 780, y = 810)

Autoscroll.select()

#log scrollbar
frameScroll = Frame(root)
#frameScroll.place(x = 18, y = 70)
global scroll_bar
scroll_bar = Scrollbar(frameScroll)
global myLog
myLog = Listbox(frameScroll, yscrollcommand = scroll_bar.set,  font = ("Verdana", 10))
#myLog.pack( side = LEFT, fill = BOTH, expand= True )
#scroll_bar.pack( side = RIGHT, fill = Y, expand= True)
scroll_bar.config(command = myLog.yview)

global labelFile
labelFile = Label(root, text = "", font = ("Verdana", 20))
labelFile.grid(row = 9, column = 0, sticky = N)

global labelTime
labelTime = Label(root, text = str(datetime.datetime.now())[:-7], font = ("Verdana", 18))
labelTime.grid(row = 0, column = 0)

root.columnconfigure(0, weight=20)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=4)

for x in range(2, 11):
    root.rowconfigure(x, weight = 80)

frameScroll.grid(row = 2, column= 0, rowspan=7, columnspan=2, sticky = NSEW, padx = 20)
myLog.pack(side = LEFT, fill = BOTH, expand = True )
scroll_bar.pack(side = RIGHT, fill = Y)


Play.grid(row = 2, column = 2, padx = 40, pady = 2, sticky = NSEW )
Pause.grid(row = 3, column = 2, padx = 40, pady = 2, sticky = NSEW )
Stop.grid(row = 4, column = 2, padx = 40, pady = 2, sticky = NSEW )
newFile.grid(row = 5, column = 2, padx = 40, pady = 2, sticky = NSEW )
recalibrate.grid(row = 6, column = 2, padx = 40, pady = 2, sticky = NSEW )
newSensorDelay.grid(row = 7, column = 2, padx = 40, pady = 2, sticky = NSEW )
newWarningSetup.grid(row = 8, column = 2, padx = 40, pady = 2, sticky = NSEW )
newTransducer.grid(row = 9, column = 2, padx = 40, pady = 2, sticky = NSEW )
Autoscroll.grid(row = 9, column = 1, sticky = NW)

global reading
reading = False
global newStart
newStart = True
global conditions
conditions = False
global COMset 
COMset = False
global sensorDelay
global newFilebool
newFilebool = True
global newSD
newSD = True
global warningSetup
warningSetup = False
global emailWarning
global paramPLimit
global newPSI
newPSI = True
global transducerPSI

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
            file.write("Time,PressureIn,PressureOut,PressureDifference,TempIn,TempOut\n")  
            newStart = False
            myLog.insert(END, "Time,PressureIn,PressureOut,PressureDifference,Temperature")
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
        else:
            messagebox.showinfo('Warning', 'You must pause or stop the program')

def new_transducer(b): #when button clicked
    global reading
    global newPSI
    global conditions
    if conditions == False: 
        popupwin()
    else:
        if reading == False:
            newPSI = True
            popupwin()
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
    myLog.insert(END, str(datetime.datetime.now())[:-7]+", "+string+" \n")
    scroll_bar.config(command = myLog.yview)
    if Autoscrollvar.get() == 1:
        myLog.yview(END)

def removeWidget(widget):
    widget.destroy()


#close the popup window
def close_win(top):
    #arduino setup
    global root

    #top.grab_release()
    wait = Toplevel(root)
    #loading = Message(wait, text="Please be patient", padx=20, pady=20)
    #loading.pack()
    wait.title('Loading... Please be patient')
    wait.geometry("600x20")
    #wait.grab_set()
    wait.lift()

    global conditions#whether everything has been met or not for read() to work

    global inputCOM #COM entry box
    global fName #fileName entry box
    global dName #sensor delay entry box
    global eName #email entry box
    global pName #pressure limit parameter entry box
    global tName #pressure transducer entry box

    global csvnamed #name of CSV file
    global arduino_port # serial port of Arduino
    global sensorDelay # delay in milliseconds
    global emailWarning #actual email
    global paramPLimit #actual parameter
    global transducerPSI # actual PSI

    global COMset #if the COM been set already or not (because you cannot change the COM once the program has started)
    global newSD #if we need a new sensor delay
    global newFilebool #if we need a new file
    global warningSetup # if the warning system is set up
    global newPSI # if we neeed a new transducer PSI

    if COMset == False:
        arduino_port = inputCOM.get()
    if newFilebool == True:
        csvnamed = fName.get()
        #Cover = Label(root, bg = "white", width = 75, height = 5)
        #Cover.place(x = 0, y = 825)
    if newSD == True:  
        sensorDelay = dName.get()
    if newPSI == True:
        transducerPSI = tName.get()
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
            if(conditions == True):
                buttonHelper("NEW WARNING SETUP "+emailWarning)
        except Exception as e:
            emailWarning = ""
            messagebox.showinfo('Warning', 'The email you provided is not valid!')
            print(e) #not sure how this part works

    #this checks that the variable either has a value or isn't needed
    tempbool = (arduino_port != "" or COMset == True)
    tempbool1 = (csvnamed!= ""or newFilebool == False)
    tempbool2 = ((sensorDelay != "") or newSD == False)
    tempbool3 = ((emailWarning != "" and paramPLimit != "") or warningSetup == True)
    tempbool4 = ((transducerPSI != "") or newPSI == False)

    if tempbool and tempbool1 and tempbool2 and tempbool3 and tempbool4:

        baud = 9600  # arduino uno runs at 9600 baud
        replace = ""
        canCloseBool = True

        if COMset == False:
            global ser
            ser = serial.Serial(arduino_port, baud)
            #print("Connected to Arduino port:" + arduino_port)
            COMset = True
            time.sleep(3) #let arduino settle down before sensor delay
        if newSD == True:
            ser.write(("sd "+str(sensorDelay)).encode())
            time.sleep(3)# let arduino settle down before PSI
            #print("Sensor Delay set to: "+ str(sensorDelay))
            newSD = False
            if(conditions == True):
                buttonHelper("NEW SENSOR DELAY "+str(sensorDelay))
        if newPSI == True:
            ser.write(("psi "+str(transducerPSI)).encode())
            #print("max PSI set to: "+ str(transducerPSI))
            newPSI = False
            if(conditions == True):
                buttonHelper("NEW TRANSDUCER PSI "+str(transducerPSI))
        if newFilebool == True:
            if os.path.exists(fName.get()):
                replace = messagebox.askquestion('Warning', "\""+fName.get()+"\" already exists. Do you want to replace it?")

            if replace == "" or replace == "yes":
                global file
                file = open(fName.get(), "w") # w for new file and a for add to existing file
                #print("Created file "+csvnamed)
                newFilebool = False
                myLog.delete(0, END) # this line and the one below used to be in newFileButton
                AGP.clear_data()
                global newStart
                newStart = True
            else:
                canCloseBool = False
        wait.destroy()

        if canCloseBool == True:
            conditions = True
            top.destroy()
            top.grab_release()
            global opened
            opened = False


def explicitClose():
    global newFilebool
    global newSD
    global warningSetup
    global newPSI
    global top
    if(conditions == True):
        newFilebool = False
        newSD = False
        warningSetup = True
        newPSI = False
    top.destroy()
    top.grab_release()

#open the Popup Dialogue
def popupwin():
    #Create a Toplevel window
    global root
    global top
    top = Toplevel(root)
    top.geometry("1250x500")

    top.grab_set()
    top.protocol("WM_DELETE_WINDOW", explicitClose)
    global COMset
    global newFilebool
    global newSD
    global warningSetup
    global newPSI

    top.resizable(False, False)

    top.columnconfigure(0, weight = 5)
    top.columnconfigure(1, weight = 10)
    top.columnconfigure(2, weight = 2)
   
    if COMset == False:
        #Create an Entry Widget in the Toplevel window
        lCOM = Label(top, text="COM Port (ex. \"COM5\" or \"COM3\",\n check this in Device Manager): " )
        #lCOM.place(x = 10, y = 10)
        lCOM.grid(row = 0, column = 0, sticky = W, padx = 1, pady = 1)
        global inputCOM
        inputCOM = Entry(top, width= 40,  font = ("Verdana", 15))
        inputCOM.grid(row = 0, column = 1, columnspan = 2, sticky = W, padx = 2, pady = 2)
        #inputCOM.place(x = 375, y = 10)
        inputCOM.insert(0, "")
    if newFilebool == True:
        Lfname = Label(top, text="File Name: ")
        #Lfname.place(x = 10, y = 50)
        Lfname.grid(row = 1, column = 0, sticky = W, padx = 1, pady = 1)
        global fName
        fName = Entry(top, width= 40,  font = ("Verdana", 15))
        #fName.place(x = 375, y = 50)
        fName.grid(row = 1, column = 1, columnspan = 2, sticky = W, padx = 1, pady = 2)
        fName.insert(0, str(datetime.datetime.now())[0:10]+"analog-data.csv")
    if warningSetup == False:
        emailName = Label(top, text="Email (for warnings): ")
        #emailName.place(x = 10, y = 90)
        emailName.grid(row = 2, column = 0, sticky = W, padx = 1, pady = 2)
        global eName
        eName = Entry(top, width= 40,  font = ("Verdana", 15))
        #eName.place(x = 375, y = 90)
        eName.grid(row = 2, column = 1, columnspan= 2, sticky = W, padx = 1, pady = 2)

        paramName = Label(top, text="Pressure Limit in psi (for email warnings): ")
        #paramName.place(x = 10, y = 130)
        paramName.grid(row = 3, column = 0, sticky = W, padx = 1, pady = 2)
        global pName
        pName = Entry(top, width= 40,  font = ("Verdana", 15))
        #pName.place(x = 375, y = 130)
        pName.grid(row = 3, column = 1, columnspan= 2, sticky = W, padx = 1, pady = 2)
    if newSD == True:
        Delayname = Label(top, text="Sensor Delay in milliseconds: ")
        #Delayname.place(x = 10, y = 170)
        Delayname.grid(row = 4, column = 0, sticky = W, padx = 1, pady = 2)
        global dName
        dName = Entry(top, width= 40,  font = ("Verdana", 15))
        #dName.place(x = 375, y = 170)
        dName.grid(row = 4, column = 1, columnspan= 2, sticky = W, padx = 1, pady = 2)
        dName.insert(0, "1000")

    if newPSI == True:
        TransdPSI = Label(top, text="Transducer PSI: ")
        #TransdPSI.place(x = 10, y = 210)
        TransdPSI.grid(row = 5, column = 0, sticky = W, padx = 1, pady = 2)
        global tName
        tName = Entry(top, width= 40,  font = ("Verdana", 15))
        #tName.place(x = 375, y = 210)
        tName.grid(row = 5, column = 1, columnspan= 2, sticky = W, padx = 1, pady = 2)
        tName.insert(0, "30")
    
    for x in range(6, 9):
        top.rowconfigure(x, weight = 1)

    #Create a Button Widget in the Toplevel Window
    button= Button(top, text="Ok", command=lambda:close_win(top))
    #button.place(x = 1100, y = 425)
    button.grid(row = 10, column=2, sticky=NSEW, padx=4, pady=10)
    
def read():
    global root
    if conditions:
        global reading
        global csvnamed
        global ser
        getData = str(ser.readline())
        data = getData[2:-5]
        if reading:

            # Indices:
            try:
                PressureIN = data[:data.index(",")]
                PressureOUT = data[data.index(",")+1 : data.index(",", data.index(",")+1)]
                PressureDIFF = data[data.index(",", data.index(",")+1)+1: data.index(",", data.index(",", data.index(",")+1)+1)]

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
    global labelTime
    labelTime.config(text = str(datetime.datetime.now())[:-7])

    #label for filename under the log
    global labelFile
    labelFile.config(text = csvnamed)
    
    #global sensorDelay
    root.grab_set()
    root.after(1000, read) #sensordelay + needs to match arduino sensor delay

my_menu = Menu(root)
root.config(menu=my_menu)
global csvnamed
csvnamed = ""

root.after(1000, read)

root.mainloop()


