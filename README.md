# Telematics
Sample project for interview

## exploration.py
This file focus on the data exploration and formation of ideas.

## trip.py
This file focus on the data preprocessing, merge and data visualization.

Raw data:
- The programs in trip.py is designed to let user select data. 
- Please note that the data needed is indicated on the top of window (first car / obd2 data, and then cell/mobile data). Choose the data in a wrong order might cause naming problems
- The source data type is limited to .gz file to avoid unintended mistakes of choosing wrong type of data

Result:
Please note that the observation / row number in the final dataset (matched_trip.csv) is more than the number of matched trips (plots in match_trip.pdf). This is because some of the trips are not one-on-one match.

## match_trip.pdf
This file includes all the plots for matched trips

## matched_trip.csv
This file includes all the trip_id and timestamp for the matched trips.
