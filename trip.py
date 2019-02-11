import gzip
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_pdf import PdfPages
from pandas.io.json import json_normalize

import tkinter as tk
from tkinter import filedialog
import os

# Let user decide which file to be uploaded
application_window = tk.Tk()
my_filetypes = [('GZ File', '.gz')]
answer_car = filedialog.askopenfilename(parent=application_window,
                                    initialdir=os.getcwd(),
                                    title="Please select a file for car/obd2 data:",
                                    filetypes=my_filetypes)
answer_cell = filedialog.askopenfilename(parent=application_window,
                                    initialdir=os.getcwd(),
                                    title="Please select a file for cell/mobile data:",
                                    filetypes=my_filetypes)
# Read data from a gzip compressed json to lists
with gzip.open(answer_car, "rt", encoding="utf-8") as f:
    car_trip = json.load(f)

with gzip.open(answer_cell, "rt", encoding="utf-8") as f:
    cell_trip = json.load(f)

# Transform the data from nested lists to pandas dataframes. Since timestamp data, no need to sort time variable.
def append_data(rawdata):
    newdata = pd.DataFrame()

    for i in range(len(rawdata)):
        newdata = newdata.append(json_normalize(data = rawdata[i]))
    return newdata


cell = append_data(cell_trip)
car = append_data(car_trip)

# Change the accuracy of timestamp in car data to be seconds
car.timestamp = 1000*car.timestamp


# Calculate durations of each trip

# Define a function to separate different trips. Assume the starting point and ending point are 0 speed
# (No one can jump on or off a driving car)
def trip_duration(data, a, b):
    data['trip_no'] = 0
    for i in range(1, len(data)):
        if data.iloc[i, a] == 0:
            data.iloc[i, b] = data.iloc[i-1, b] + 1
        else:
            data.iloc[i, b] = data.iloc[i-1, b]
    return data

# Group data by different trips
def group_trip(data):
    group_data = data.groupby('trip_no').agg({'trip_id': 'min', 'timestamp': 'min', 'speed':'min'})
    group_data['length'] = data[['trip_no', 'timestamp']].groupby('trip_no').agg(lambda x: x.max() - x.min())
    group_data = group_data.query('length >5 ')

    return group_data

car = trip_duration(car, 0, 3)
cell = trip_duration(cell, 2, 5)

group_car = group_trip(car)
group_cell = group_trip(cell)


# Search for the closed length to merge.
# Exact time length match is not used due to the different timestamp interval used.
df_match = pd.merge_asof(group_car.reset_index().sort_values(by='length'),
                           group_cell.reset_index().sort_values(by='length'),
                           suffixes=['_cell', '_car'],
                           on='length',
                           direction='nearest')

# Filter trip which doesn't have a 0 start speed (Mainly the first one due to trip_no). Drop speed due to redundancy.
df_match = df_match.query('speed_cell ==0  & speed_car == 0')
df_match = df_match.drop(['speed_cell', 'speed_car'], axis=1)

# Save the matched trip data to csv
df_match.to_csv('matched_trip.csv')

# Select matched trips speed data for later plotting
with PdfPages('matched_trip.pdf') as pdf:
    for i in range(len(df_match)):
        trip_index_cell = df_match.loc[i, 'trip_no_cell']
        trip_index_car = df_match.loc[i, 'trip_no_car']

        if max(cell.query('trip_no == @trip_index_cell')['speed']) > 0:
            plt.plot(
                cell.query('trip_no == @trip_index_cell')['timestamp'],
                cell.query('trip_no == @trip_index_cell')['speed'])
            plt.ylabel('Speed')
            plt.xlabel('Timestamp: (epoch) seconds')
            filename = 'matched_trip_' + str(i)
            plt.title(filename)
            pdf.savefig()  # saves the current figure into a pdf page
            plt.close()
