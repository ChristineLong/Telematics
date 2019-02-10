import gzip
import json
import pandas as pd
import numpy as np

from pandas.io.json import json_normalize


# Read data from a gzip compressed json to lists
with gzip.open("obd2_trips.json.gz", "rt", encoding="utf-8") as f:
    car_trip = json.load(f)

with gzip.open("mobile_trips.json.gz", "rt", encoding="utf-8") as f:
    cell_trip = json.load(f)

# Transform the data from nested lists to pandas dataframes. Since timestamp data, no need to sort by time variable.
def append_data(rawdata):
    newdata = pd.DataFrame()

    for i in range(len(rawdata)):
        newdata = newdata.append(json_normalize(data = rawdata[i]))
    return newdata

cell = append_data(cell_trip)
car = append_data(car_trip)

# Explore data
print(cell.shape)
print(car.shape)

print(car.describe())
print(cell.describe())
# All speed is no less than 0. No need for filtering.
# Timestamp in car is not epoch. Cannot used for matching.
# Also, by comparison to cell, the accuracy for it should be 1000 seconds.


print(len(np.unique(cell['trip_id'])))
print(len(np.unique(car['trip_id'])))
# Trip ids are different in two dataframes. Cannot be used for match.




