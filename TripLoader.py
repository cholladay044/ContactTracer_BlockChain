import pandas as pd

"""import os
from json import loads"""


class TripLoader:

    def __init__(self, trips_file):
        self.data_frame = pd.read_csv(trips_file)
        """
        fileSize = os.path.getsize(trips_file)

        trips = []
        progress = 0
        with open(trips_file, 'r') as inputFile:
            for line in inputFile:
                progress = progress + len(line)
                progressPercent = (1.0 * progress) / fileSize
                trips.append(loads(line))
                # if progressPercent % 1 == 0:
                print(progressPercent * 100, "%")

        print("\nBuilding DataFrame")
        rows = []
        i = 0
        prev = 0
        for trip in trips:
            i += 1
            progress = i / len(trips) * 100
            if int(progress) != prev:
                prev = int(progress)
                print(str(int(progress)), "%")
            for feature in trip['route']['features']:
                id = trip['vehicle_id']
                latitude = feature['geometry']['coordinates'][0]
                longitude = feature['geometry']['coordinates'][1]
                timestamp = feature['properties']['timestamp']

                rows.append({'user_id': id, 'latitude': latitude, 'longitude': longitude, 'timestamp': timestamp})
                self.data_frame = pd.DataFrame.from_records(rows)
                vehicles = self.data_frame.user_id.unique()
                self.data_frame['user_id'] = self.data_frame['user_id'].replace(vehicles,
                                                                                [vehicles.tolist().index(x) + 1 for x in
                                                                                 vehicles])
                self.data_frame.sort_values(by="timestamp")
        print("Finished Loading")"""

    def data(self):
        return self.data_frame
