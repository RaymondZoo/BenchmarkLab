from ast import Constant
from datetime import datetime
from tokenize import String
import matplotlib.pyplot as plt
import numpy as np
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
file = open('testdata.csv', encoding = 'utf-8-sig')
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
    rawTime.append(row[0])
    
    if (row[1] == " START " or row[1] == " RECALIBRATE " or  row[1] == " NEW SENSOR DELAY "):
        pressDiff.append(0)
    elif (row[1] == " PAUSE "):
        pressDiff.append(pressDiff[len(pressDiff) - 1])
    else:
        pressDiff.append(float(row[2]))
print(rawTime)
print(pressDiff)

# Finished reading a file
file.close()

# ***** PROCESSING DATA *****
# Variables for graphing
timeGraph = []
pressDiffGraph =  []

# Graph raw data if timeInterval is not specified;
# Otherwise, get average of time interval
if timeInterval == 0:
    pressDiffGraph = pressDiff
    for i in range(len(rawTime)):
        timeGraph.append((datetime.strptime(rawTime[i], '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(rawTime[0], '%Y-%m-%d %H:%M:%S.%f')).total_seconds() * 1000)
# TODO: Make averages depending on time interval size
# else:
#     sumTime = 0.0
#     sumPress = 0.0
#     for i in range(len(rawTime)):
#         # If sumTime divisible by timeInterval, then append avg to timeGraph and pressDiffGraph
#         # Reset averages
#         timeGraph.append((datetime.strptime(rawTime[i], '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(rawTime[0], '%Y-%m-%d %H:%M:%S.%f')).total_seconds() * 1000)
#     timeGraph
#     pressDiffGraph.append()
timeGraph = [float(x) for x in timeGraph]


# ***** GRAPHING *****
# Graph values onto a plot
plt.plot(timeGraph, pressDiffGraph, color = 'b', linestyle = 'dashed', marker = 'o', label = "Control")
plt.xticks(rotation = 25)

# Display graph
plt.title('Pressure Over Time', fontsize = 20)
plt.xlabel('Time (ms)')
plt.ylabel('Pressure')

plt.grid()
plt.legend()
plt.show()