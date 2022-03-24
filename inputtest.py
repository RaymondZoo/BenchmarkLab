#Import the required library
from tkinter import*

#Create an instance of tkinter frame
win= Tk()

#Define geometry of the window
win.geometry("750x250")

#Define a function to close the popup window
def close_win(top):
   top.destroy()

#Define a function to open the Popup Dialogue
def popupwin():
   #Create a Toplevel window
   top= Toplevel(win)
   top.geometry("750x200")

   #Create an Entry Widget in the Toplevel window
   LCOM = Label(top, text="COM Port: ")
   LCOM.place(x = 10, y = 10)
   inputCOM = Entry(top, width= 25,  font = ("Verdana", 15))
   inputCOM.place(x = 375, y = 10)

   Lfname = Label(top, text="File Name: ")
   Lfname.place(x = 10, y = 50)
   fName = Entry(top, width= 25,  font = ("Verdana", 15))
   fName.place(x = 375, y = 50)

   #Create a Button Widget in the Toplevel Window
   button= Button(top, text="Ok", command=lambda:close_win(top), width = 5)
   button.place(x = 660, y = 100)

popupwin()
win.mainloop()