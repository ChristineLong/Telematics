import gzip
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pandas.io.json import json_normalize


# Read data from a gzip compressed json to lists
with gzip.open("obd2_trips.json.gz", "rt", encoding="utf-8") as f:
    car_trip = json.load(f)

with gzip.open("mobile_trips.json.gz", "rt", encoding="utf-8") as f:
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
# car
def trip_duration(data, a, b):
    data['trip_no'] = 0
    for i in range(1, len(data)):
        if data.iloc[i, a] == 0:
            data.iloc[i, b] = data.iloc[i-1, b] + 1
        else:
            data.iloc[i, b] = data.iloc[i-1, b]
    return data

def group_trip(data):
    group_data = data.groupby('trip_no').agg({'trip_id': 'min', 'timestamp': 'min','speed': 'min'})
    group_data['length'] = data[['trip_no', 'timestamp']].groupby('trip_no').agg(lambda x: x.max() - x.min())
    group_data = group_data.query('length >5 ')

    return group_data

car = trip_duration(car, 0, 3)
cell = trip_duration(cell, 2, 5)

group_car = group_trip(car)
group_cell = group_trip(cell)


# search for the closed length to merge
df_match = pd.merge_asof(group_car.reset_index().sort_values(by='length'),
                           group_cell.reset_index().sort_values(by='length'),
                           suffixes=['_cell', '_car'],
                           on='length',
                           direction='nearest')

df_match['trip_index'] = range(1,len(df_match)+1)

# Select matched trips speed data for later plotting

car_speed = pd.DataFrame()
for i in range(len(df_match)):
    car_speed = car_speed.append(car[(car['trip_no'] == df_match.loc[i, 'trip_no_car'])])


cell_speed = pd.DataFrame()
for i in range(len(df_match)):
    cell_speed = cell_speed.append(cell[(cell['trip_no'] == df_match.loc[i, 'trip_no_cell'])])





for i in range(len(df_match)):
    trip_index_cell = df_match.loc[i,'trip_no_cell']
    trip_index_car = df_match.loc[i,'trip_no_car']


    if max(cell.query('trip_no == @trip_index_cell')['speed']) > 0  \
        and max(car.query('trip_no == @trip_index_car')['speed']) > 0 \
            and min(cell.query('trip_no == @trip_index_cell')['speed']) == min(car.query('trip_no == @trip_index_car')['speed']):
        plt.plot(
            cell.query('trip_no == @trip_index_cell')['timestamp'],
            cell.query('trip_no == @trip_index_cell')['speed'])
        plt.plot(
            cell.query('trip_no == @trip_index_cell')['timestamp'],
            car.query('trip_no == @trip_index_car')['speed'])

    filename = 'matched_trip_' + str(i) + '.png'
    plt.savefig(filename)  # save the figure to file
