from ast import Constant
from datetime import datetime
from tokenize import String
from drawnow import *
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import csv
import time

# Variables, must only be altered by reading line inputs
raw_time = []
press = []
fig, ax = plt.subplots()
# fig = Figure(figsize = (5, 4), dpi = 200)
# ax = fig.add_subplot()

# ***** READING LINE INPUTS *****
def read_line_inputs(str_read):
    # Prerequisite: ONLY PUT IN DATA THAT HAS NUMBERS
    col = 0
    new_data = True
    
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
    press[len(raw_time) - 1] = float(press[len(raw_time) - 1])
    return [raw_time, press]

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
        if not(row[1] == " START " or row[1] == " RECALIBRATE " or  row[1] == " NEW SENSOR DELAY " or row[1] == " PAUSE " or row[1] == " STOP "):
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
    
    drawnow
    # plt.show()
    plt.pause(.000001)

def change_graph_units(proc_data, unit_in_ms):
    if unit_in_ms != 0:
        for i in range(len(proc_data[0])):
            proc_data[0][i] = proc_data[0][i] / unit_in_ms
    return proc_data

def clear_data():
    ax.clear()
    global raw_time
    raw_time = []
    global press
    press = []

raw_data = read_file()
proc_data = process_data(raw_data)
graph_data(proc_data)