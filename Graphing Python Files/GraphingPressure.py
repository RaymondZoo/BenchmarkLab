from ast import Constant
from datetime import datetime
from tokenize import String
import matplotlib.pyplot as plt
import numpy as np
import time
import csv


# ***** VARIABLES *****
# CSV values
rawTime = []
pressDiff = []

# Scale data by this amount of time
try:
    timeInterval = eval(input("How Much time Between Intervals (in ms): "))
except NameError:
    print("Invalid input")


# ***** READING CSV FILE *****
# Open file
file = open('thirdtest.csv', encoding = 'utf-8-sig')
type(file)
csvreader = csv.reader(file)

# Read all of the headers
header = []
for row in csvreader:     
    # Add first row
    header.append(row)
    break
print(header)

# Gather data from CSV file
lines = csvreader
for row in lines:
    rawTime.append((row[0]))
    pressDiff.append(float(row[1]))
print(rawTime)
print(pressDiff)

# Finished reading a file
file.close()

# ***** PROCESSING DATA *****
# Variables for graphing
timeGraph = []

# If there are pauses, use previous pressure
for i in range(len(pressDiff)):
    if (pressDiff[i] == "PAUSED"):
        pressDiff[i] == pressDiff[i - 1]

# Graph raw data if timeInterval is not specified;
# Otherwise, get average of time interval
if timeInterval == 0:
    for i in range(len(rawTime)):
        timeGraph.append((datetime.strptime(rawTime[i], '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(rawTime[0], '%Y-%m-%d %H:%M:%S.%f')).total_seconds() * 1000)
# else:
#   


# ***** GRAPHING *****
# Graph values onto a plot
plt.plot(timeGraph, pressDiff, color = 'b', linestyle = 'dashed', marker = 'o', label = "Control")
plt.xticks(rotation = 25)

# Display graph
plt.title('Pressure Over Time', fontsize = 20)
plt.xlabel('Time (ms)')
plt.ylabel('Pressure')

plt.grid()
plt.legend()
plt.show()