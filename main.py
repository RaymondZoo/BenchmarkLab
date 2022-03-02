import random

from tkinter import *
from tkinter import messagebox

#set up frame

root = Tk()
root.title('Flow Loop Testing')
root.resizable(0, 0)
myCanvas = Canvas(root, width = 900, height = 700, bg = "White")
myCanvas.pack()


#logo
fileName = "Benchmark.gif"
pic = PhotoImage(file = fileName)
#resizedPic = pic.subsample(18, 18)

logo = Label(root, image = pic)
logo.photo = pic #ensures label doesn't stay blank
logo.pack()
logo.place(x = 675, y = 10)
logo.config(width=200, height = 200)

#buttons
Play = Button(root, height = 5, width = 20, bg = "green", text = "Play", command=lambda: play_click(Play)) #makes button
Play.pack()
Play.place(x = 675, y = 100)

Pause = Button(root, height = 5, width = 20, bg = "yellow", text = "Pause", command=lambda: pause_click(Pause)) #makes button
Pause.pack()
Pause.place(x = 675, y = 190)

Stop = Button(root, height = 5, width = 20, bg = "red", text = "Stop", command=lambda: stop_click(Stop)) #makes button
Stop.pack()
Stop.place(x = 675, y = 280)


def play_click(b): #when button clicked
    return
def pause_click(b): #when button clicked
    return
def stop_click(b): #when button clicked
    return
    

my_menu = Menu(root)
root.config(menu=my_menu)




root.mainloop()

