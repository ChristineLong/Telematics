# Telematics
Sample project for interview. Following files are included in this repository.

## exploration.py
This file focus on the data exploration and deduction of ways to merge.

## trip.py
This file focus on the data preprocessing, merge and data visualization.

Raw data:
- The programs in trip.py is designed to let user select data. 
- Please note that the data needed is indicated on the top of window (first car / obd2 data, and then cell/mobile data). Choose the data in a wrong order might cause naming problems
- The source data type is limited to .gz file to avoid unintended mistakes of choosing wrong type of data

Result:
- The final dataset (matched_trip.csv) contains trip number, timestamps for different sources (car and mobile) and length of the trip. The matched trips are also presented in plots (plots in match_trip.pdf). Note that some of the trips are not one-on-one match.
- Please also note that matched_trip_no is different from cell trip_no or car trip_no. It is used to refer to matched trip.

## match_trip.pdf
This file includes all the plots for matched trips

## matched_trip.csv
This file includes all the trip_id and timestamp for the matched trips.


## Methodology and findings:
Method:
The method of matching trips is by the length of trip. Due to different trips started and ended in different time, the start/end point of the trip shouldn't be timestamp corresponding to different trip id. Therefore, new trip ids (trip_no) are assigned according to the speed. When the speed reaches 0, it will be identified as start / end point of a trip. By using trip_no, the trips for car and mobile are divided to different new trips, and these trips are matched by their length. Moreover, the trip with maximum speed 0 is also removed, since there is no point in matching two "trips" when neither the car nor the cell moves.

Results:
There are 48 matched trips. Most trips have relatively stable change of speed, indicating that the driver’s driving behavior is relatively not risky. Meanwhile five of them (matched_trip_no: 18, 47, 52, 149, 312) have more than three times of abrupt speed changes. Using the information of the timestamp, the time of these five trips are as follows (assuming the trips is in EST):
Sunday, June 4, 2017 11:08:39 AM
Sunday, May 21, 2017 1:49:41 PM
Sunday, May 14, 2017 3:06:42 PM
Sunday, June 4, 2017 12:30:34 PM
Tuesday, May 30, 2017 10:54:07 PM
As we can see, 4 out of five trips were around Sunday noon. Given that the timestamp didn’t focus on Sunday(date=(timestamp/86400)+25569), and assuming the owner was the driver the whole time, this could be the consequence of a more complicated traffic condition during Sunday noon, or certain habits/activities patterns in the driver’s life during Sunday noon.
