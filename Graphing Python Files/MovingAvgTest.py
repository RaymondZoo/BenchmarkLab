from ast import Constant
from datetime import datetime
from tokenize import String
import matplotlib.pyplot as plt
import numpy as np
import sys
import csv

# ***** READING CSV FILE *****
def read_file():
    # CSV values
    raw_time = []
    press_diff = []

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
            raw_time.append(row[0])
            press_diff.append(float(row[1]))

    # Finished reading a file
    file.close()
    return [raw_time, press_diff]

# ***** PROCESSING DATA *****
def processData(raw_data):
    # Variables for graphing
    proc_time = []

    # Process the raw time into intervals
    for i in range(len(raw_data[0])):
        proc_time.append((datetime.strptime(raw_data[0][i], '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(raw_data[0][0], '%Y-%m-%d %H:%M:%S.%f')).total_seconds() * 1000)
        proc_time = [float(x) for x in proc_time]

    # Scale data by this amount of time
    try:
        avg_duration = eval(input("How Much Time Between Intervals (in ms): "))
    except NameError:
        print("Invalid input")

    # Graph raw data if avg_duration is not specified;
    # Otherwise, get average of time interval
    if avg_duration == 0:
        return [proc_time, raw_data[1]]
    else:
        return getAvgData([proc_time, raw_data[1]], avg_duration)

def getAvgData(unscaled_data, avg_duration):
    # Variables
    avg_time = []
    avg_press_diff = []
    
    start_time = 0
    count = 0
    time_sum = 0
    press_sum = 0
    
    # Do a loop start beginning of the time  to increase avg_duration
    for i in range(len(unscaled_data[0])):
        if (unscaled_data[0][i] >= start_time and unscaled_data[0][i] < start_time + avg_duration):
            # Update sums
            time_sum = time_sum + unscaled_data[0][i]
            press_sum = press_sum + unscaled_data[1][i]
            count = count + 1
        else:
            # Show raw data if the time passed as parameter is too small
            if count == 0:
                return unscaled_data
            else:
                # Append avg values
                avg_time.append(time_sum / count)
                avg_press_diff.append(press_sum / count)
                
                # Reset values
                start_time = unscaled_data[0][i]
                count = 0
                time_sum = 0
                press_sum = 0
    return [avg_time, avg_press_diff]

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
    
    # Graph values onto a plot
    plt.plot(proc_data[0], proc_data[1], color = 'b', linestyle = 'dashed', marker = 'o', label = "Control")
    plt.xticks(rotation = 25)
    
    # Display graph
    plt.title('Pressure Over Time', fontsize = 20)
    plt.xlabel('Time (' + unit_name + ')')
    plt.ylabel('Pressure')
    plt.grid()
    plt.legend()
    plt.show()

def change_graph_units(proc_data, unit_in_ms):
    if unit_in_ms != 0:
        for i in range(len(proc_data[0])):
            proc_data[0][i] = proc_data[0][i] / unit_in_ms
    return proc_data

raw_data = read_file()
proc_data = processData(raw_data)
graph_data(proc_data)