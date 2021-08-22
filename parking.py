import datalab.bigquery as bq
import pandas as pd
# import folium
from google.cloud import storage
import geohash
from sklearn.preprocessing import MinMaxScaler
# from folium.plugins import HeatMap

from pandas.io.json import json_normalize

# Extract data from SearchingForParking table
latitude = 30
longitude = -98
def implicit():


    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)
SQL = """
  %%bigquery parking
  select * , TotalSearching/(TotalSearching/(PercentSearching)) as SearchingForParkingRatio
  from `geotab-public-intelligence.UrbanInfrastructure.SearchingForParking`
  where Latitude> @ minLat and Latitude < @ maxLat and Longitude < @ maxLng and Longitude > @ minLng;

"""

query_parameters = [
    {
        'name': 'minLat',
        'parameterType': {'type': 'INTEGER'},
        'parameterValue': {'value': latitude - 0.5}
    },
    {
        'name': 'maxLat',
        'parameterType': {'type': 'INTEGER'},
        'parameterValue': {'value': latitude + 0.5}
    },
    {
        'name': 'minLng',
        'parameterType': {'type': 'INTEGER'},
        'parameterValue': {'value': longitude - 0.5}
    },
    {
        'name': 'maxLng',
        'parameterType': {'type': 'INTEGER'},
        'parameterValue': {'value': longitude + 0.5}
    }
]

summary = bq.Query(SQL, job_config=query_parameters).to_dataframe(dialect='standard')

# Decode Geohash into latitude and longitude
summary['Latitude'] = summary.apply(lambda row: geohash.decode(row.Geohash)[0], axis=1)
summary['Longitude'] = summary.apply(lambda row: geohash.decode(row.Geohash)[1], axis=1)

# Calculate Searching for Parking Index and scale it to range from 1 to 10
a = 0.3
b = 0.7

summary['Index_tmp'] = summary.apply(lambda row: a * row['SearchingForParkingRatio'] + b * row['AvgTimeToParkRatio'],
                                     axis=1)

IndexMax = summary.Index_tmp.mean() + 3 * summary.Index_tmp.std()
ScaleData = summary[summary.Index_tmp <= IndexMax]
scaler = MinMaxScaler(feature_range=(0, 10)).fit(pd.DataFrame(ScaleData.Index_tmp))
summary['Index'] = scaler.transform(pd.DataFrame(summary.Index_tmp))
summary = summary.round({'Index': 2})

summary['Index'] = summary.apply(lambda row: 10 if row['Index'] > 10 else row['Index'], axis=1)
# If dictionary
# key_min = min(summary.keys(), key=(lambda k: summary[k]))
# Parking = summary[key_min]
# If list
Parking = min(summary)

