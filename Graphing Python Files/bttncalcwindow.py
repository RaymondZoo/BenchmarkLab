from tkinter import *
from tkinter import ttk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from datetime import datetime
import numpy as np
import csv


root = Tk()
root.wm_title("Embedding in Tk")

fig = Figure(figsize=(5, 4), dpi=100)
t = np.arange(0, 3, .01)
ax = fig.add_subplot()
raw_time = []
press = []
# Scale data by this amount of time
avg_duration = 0

# ***** READING LINE INPUTS *****
def read_line_inputs(str_read):
    # Prerequisite: ONLY PUT IN DATA THAT HAS NUMBERS
    col = 0
    new_data = True
    prev_size = len(raw_time)
    
    # Takes a line from a CSV input, reads it
    # Appends the data to the proper list
    for i in range(0, len(str_read)):
        character = str_read[i]
        if character == ",":
            col += 1
            new_data = True
        else:
            # Update time if we are reading time
            if col == 0:
                if new_data:
                    # New time, append to raw_time
                    raw_time.append(character)
                    new_data = False
                else:
                    # Adding to current time string
                    raw_time[len(raw_time) - 1] += character
            elif col == 3:
                if new_data:
                    # New pressure data
                    press.append(character)
                    new_data = False
                else:
                    # Adding to current data string
                    press[len(raw_time) - 1] += character
    if prev_size != len(raw_time):
        press[len(press) - 1] = float(press[len(press) - 1])
    return [raw_time, press]

# ***** READING CSV FILE *****
def read_file():
    # CSV values
    raw_time = []
    press = []

    # Open file
    file = open('20220526_Jo Mill_Data.csv', encoding = 'utf-8-sig')
    type(file)
    csvreader = csv.reader(file)

    # Read all of the headers
    header = []
    for row in csvreader:     
        # Add first row
        header.append(row)
        break

    # Gather data from CSV file
    lines = csvreader
    for row in lines:
        if not(row[1] == " START " or row[1] == " RECALIBRATE " or  row[1] == " NEW SENSOR DELAY " or row[1] == " PAUSE " or row[1] == " STOP "):
            raw_time.append(row[0])
            press.append(float(row[3]))

    # Finished reading a file
    file.close()
    return [raw_time, press]

# ***** PROCESSING DATA *****
def process_data(raw_data):
    # Variables for graphing
    proc_time = []

    # Process the raw time into intervals
    for i in range(len(raw_data[0])):
        time = (datetime.strptime(raw_data[0][i], '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(raw_data[0][0], '%Y-%m-%d %H:%M:%S.%f')).total_seconds() * 1000
        proc_time.append(float(time))

    # Graph raw data if avg_duration is not specified;
    # Otherwise, get average of time interval
    proc_press = [abs(float(x)) for x in raw_data[1]]
    if avg_duration == 0:
        return [proc_time, proc_press]
    else:
        return get_avg_data([proc_time, proc_press], avg_duration)

def get_avg_data(unscaled_data, avg_duration):
    # Variables
    avg_time = []
    avg_press = []
    start_time = 0
    nodes = 0
    time_sum = 0
    press_sum = 0
    
    # Do a loop start beginning of the time  to increase avg_duration
    for i in range(len(unscaled_data[0])):
        if (unscaled_data[0][i] >= start_time and unscaled_data[0][i] < start_time + avg_duration):
            # Update sums
            time_sum = time_sum + unscaled_data[0][i]
            press_sum = press_sum + unscaled_data[1][i]
            nodes += 1
        else:
            # Show raw data if the time passed as parameter is too small
            if nodes == 0:
                return unscaled_data
            else:
                # Append avg values
                avg_time.append(time_sum / nodes)
                avg_press.append(press_sum / nodes)
                
                # Reset values
                start_time = unscaled_data[0][i]
                nodes = 0
                time_sum = 0
                press_sum = 0
    return [avg_time, avg_press]

# ***** GRAPHING *****
def graph_data(proc_data):
    # Change the units of the time automatically
    unit_in_ms = 0
    unit_name = "ms"
    if len(proc_data[0]) > 0:
        if proc_data[0][len(proc_data[0]) - 1] >= 86400000:
            # Unit changed to hours
            unit_name = "hr"
            unit_in_ms = 3600000
        elif proc_data[0][len(proc_data[0]) - 1] >= 1200000:
            # Unit changed to minutes
            unit_name = "min"
            unit_in_ms = 60000
        elif proc_data[0][len(proc_data[0]) - 1] >= 60000:
            # Unit changed to seconds
            unit_name = "s"
            unit_in_ms = 1000
        proc_data = change_graph_units(proc_data, unit_in_ms)
    
    ax.clear()
    ax.plot(proc_data[0], proc_data[1], color = '#0d9eb7', label = "Control")
    
    ax.set_xlabel('Time (' + unit_name + ')')
    ax.set_ylabel('Pressure (psi)')
    ax.set_xlim(0)
    ax.grid(True)

def change_graph_units(proc_data, unit_in_ms):
    if unit_in_ms != 0:
        for i in range(len(proc_data[0])):
            proc_data[0][i] = proc_data[0][i] / unit_in_ms
    return proc_data

# raw_data = read_file()
# proc_data = process_data(raw_data)
# graph_data(proc_data)

# SHOW CANVAS ON FIGURE
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()

# pack_toolbar=False will make it easier to use a layout manager later on.
toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()

canvas.mpl_connect(
    "key_press_event", lambda event: print(f"you pressed {event.key}"))
canvas.mpl_connect("key_press_event", key_press_handler)


new_val = DoubleVar()
def update_graph():
    # update data
    global avg_duration
    avg_duration = float(new_val.get())
    raw_data = read_file()
    proc_data = process_data(raw_data)
    graph_data(proc_data)

    # required to update canvas and attached toolbar!
    canvas.draw()

#Initialize a Label to display the User Input
label = Label(root, text = "Time Interval (ms)", font = ("Arial 10 bold"))

#Create an Entry widget to accept User Input
entry = Entry(root, width = 40, textvariable = new_val)

button_calc = Button(root, text = "Calculate", command = update_graph)

# Packing order is important. Widgets are processed sequentially and if there
# is no space left, because the window is too small, they are not displayed.
# The canvas is rather flexible in its size, so we pack it last which makes
# sure the UI controls are displayed as long as possible.
button_calc.pack(side = BOTTOM)
entry.pack(side = BOTTOM)
label.pack(side = BOTTOM)
toolbar.pack(side = BOTTOM, fill = X)
canvas.get_tk_widget().pack(side = TOP, fill = BOTH, expand = 1)

mainloop()