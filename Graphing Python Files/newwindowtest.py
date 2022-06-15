import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from datetime import datetime
import numpy as np
import csv


root = tkinter.Tk()
root.wm_title("Embedding in Tk")

fig = Figure(figsize=(5, 4), dpi=100)
t = np.arange(0, 3, .01)
ax = fig.add_subplot()


# ***** READING CSV FILE *****
def read_file():
    # CSV values
    raw_time_f = []
    press_f = []

    # Open file
    file = open('testdata.csv', encoding = 'utf-8-sig')
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
        if not(row[1] == " START " or row[1] == " RECALIBRATE " or  row[1] == " NEW SENSOR DELAY " or row[1] == " PAUSE "):
            raw_time_f.append(row[0])
            press_f.append(float(row[1]))

    # Finished reading a file
    file.close()
    return [raw_time_f, press_f]

# ***** PROCESSING DATA *****
def process_data(raw_data):
    # Variables for graphing
    proc_time = []

    # Process the raw time into intervals
    for i in range(len(raw_data[0])):
        time = (datetime.strptime(raw_data[0][i], '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(raw_data[0][0], '%Y-%m-%d %H:%M:%S.%f')).total_seconds() * 1000
        proc_time.append(float(time))

    # Scale data by this amount of time
    avg_duration = 0

    # Graph raw data if avg_duration is not specified;
    # Otherwise, get average of time interval
    if avg_duration == 0:
        return [proc_time, raw_data[1]]
    else:
        return get_avg_data([proc_time, raw_data[1]], avg_duration)

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
    ax.plot(proc_data[0], proc_data[1], color = '#0d9eb7', marker = 'o', label = "Control")
    
    ax.set_xlabel('Time (' + unit_name + ')')
    ax.set_ylabel('Pressure (psi)')
    ax.set_xlim(0)
    ax.grid(True)

def change_graph_units(proc_data, unit_in_ms):
    if unit_in_ms != 0:
        for i in range(len(proc_data[0])):
            proc_data[0][i] = proc_data[0][i] / unit_in_ms
    return proc_data

raw_data = read_file()
proc_data = process_data(raw_data)
graph_data(proc_data)

# SHOW CANVAS ON FIGURE
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()

# pack_toolbar=False will make it easier to use a layout manager later on.
toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()

canvas.mpl_connect(
    "key_press_event", lambda event: print(f"you pressed {event.key}"))
canvas.mpl_connect("key_press_event", key_press_handler)

button_quit = tkinter.Button(master=root, text="Quit", command=root.quit)


# def update_frequency(new_val):
#     # retrieve frequency
#     f = float(new_val)

#     # update data
#     y = 2 * np.sin(2 * np.pi * f * t)
#     line.set_data(t, y)

#     # required to update canvas and attached toolbar!
#     canvas.draw()

# slider_update = tkinter.Scale(root, from_=1, to=5, orient=tkinter.HORIZONTAL,
#                               command=update_frequency, label="Frequency [Hz]")


# Packing order is important. Widgets are processed sequentially and if there
# is no space left, because the window is too small, they are not displayed.
# The canvas is rather flexible in its size, so we pack it last which makes
# sure the UI controls are displayed as long as possible.
button_quit.pack(side=tkinter.BOTTOM)
# slider_update.pack(side=tkinter.BOTTOM)
toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

tkinter.mainloop()