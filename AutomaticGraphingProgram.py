from ast import Constant
from datetime import datetime
from tokenize import String
import matplotlib as mpl
mpl.use("Qt5Agg")
from matplotlib.figure import Figure
from drawnow import *
import matplotlib.pyplot as plt
import numpy as np
import csv
import time

# Variables, must only be altered by reading line inputs
raw_time = []
press = []
fig, ax = plt.subplots()
ax.set_title("Inlet Pressure")
fig.show()

raw_time2 = []
press2 = []
fig2, ax2 = plt.subplots()
ax2.set_title("Outlet Pressure")
fig2.show()

raw_time3 = []
press3 = []
fig3, ax3 = plt.subplots()
ax3.set_title("Differential Pressure")
fig3.show()

raw_time4 = []
press4 = []
fig4, ax4 = plt.subplots()
ax4.set_title("Inlet Temperature")
fig4.show()

raw_time5 = []
press5 = []
fig5, ax5 = plt.subplots()
ax5.set_title("Outlet Temperature")
fig5.show()
#fig = plt.figure()
#fig = Figure(figsize = (5, 4), dpi = 200)
#ax = fig.add_subplot()

# need to label each figure
figuredict = {
  1: [fig, raw_time, press, ax, "Inlet Pressure", 'Pressure (PSI)'],
  2: [fig2, raw_time2, press2, ax2, "Outlet Pressure", 'Pressure (PSI)'],
  3: [fig3, raw_time3, press3, ax3, "Differential Pressure", 'Pressure (PSI)'],
  4: [fig4, raw_time4, press4, ax4, "Inlet Temperature", 'Temperature (Celsius)'],
  5: [fig5, raw_time5, press5, ax5, "Outlet Temperature", 'Temperature (Celsius)']
}

# ***** READING LINE INPUTS *****
def read_line_inputs(str_read, x):
    # Prerequisite: ONLY PUT IN DATA THAT HAS NUMBERS
    col = 0
    new_data = True
    datatemp = figuredict[x][2]
    raw_timetemp = figuredict[x][1]
    #print(str_read)
    
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
                    raw_timetemp.append(character)
                    new_data = False
                else:
                    # Adding to current time string
                    raw_timetemp[len(raw_timetemp) - 1] += character
            elif col == x:
                if new_data:
                    # New pressure data
                    datatemp.append(character)
                    new_data = False
                else:
                    # Adding to current data string
                    datatemp[len(raw_timetemp) - 1] += character
    
    datatemp[len(raw_timetemp) - 1] = float(datatemp[len(raw_timetemp) - 1])
    #print(x)
    #print(presstemp)
    return [raw_timetemp, datatemp]

# ***** READING CSV FILE *****
def read_file():
    # CSV values
    raw_time_f = []
    press_f = []

    # Open file
    file = open('ExampleCSVdata.csv', encoding = 'utf-8-sig')
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
        #if not(row[1] == " START " or row[1] == " RECALIBRATE " or  row[1] == " NEW SENSOR DELAY " or row[1] == " PAUSE " or row[1] == " STOP " or row[1] == " NEW WARNING SETUP "):
        if len(row) != 1:
            raw_time_f.append(row[0])
            press_f.append(float(row[3]))

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
    proc_press = [float(x) for x in raw_data[1]]
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
def graph_data(proc_data, x):
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

    axtemp = figuredict[x][3]
    figtemp = figuredict[x][0]
    
    axtemp.clear()
    axtemp.plot(proc_data[0], proc_data[1], color = '#0d9eb7', marker = 'o', label = "Control")
    
    axtemp.set_title(figuredict[x][4])
    axtemp.set_xlabel('Time (' + unit_name + ')')
    axtemp.set_ylabel(figuredict[x][5])
    axtemp.set_xlim(0)
    axtemp.grid(True)
    
    #drawnow
    #plt.show()
    #plt.pause(.000001)
    figtemp.canvas.draw_idle()
    figtemp.canvas.flush_events()

def change_graph_units(proc_data, unit_in_ms):
    if unit_in_ms != 0:
        for i in range(len(proc_data[0])):
            proc_data[0][i] = proc_data[0][i] / unit_in_ms
    return proc_data

def clear_data():
    for x in range(1, 6):
        figuredict[x][3].clear()
        figuredict[x][1] = []
        figuredict[x][2] = []

#FOR TESTING 
#raw_data = read_file()
#proc_data = process_data(raw_data)
#graph_data(proc_data)