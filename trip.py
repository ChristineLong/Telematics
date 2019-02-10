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

