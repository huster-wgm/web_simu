import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# columns = ['grid_id', 'time_id', 'avg_speed', 'num']
data = pd.read_csv(BASE_DIR+'/static/data/sample_500x.csv')
# initial parameters
# set bangkok range
lon_w, lon_e = 100.40, 100.70
lat_s, lat_n = 13.60, 13.90
# set time interval /min
time_interval = 30
time_range = np.arange(0, 60 * 24, time_interval) + time_interval // 2
# grid_nums and grid_interval
grid_nums = 500
grid_interval = 0.30 / grid_nums


# extract result by time period
def data_by_time(time):
    # ['grid_id','time_id','avg_speed','num']
    lon_axis = []
    lat_axis = []
    avg_speed = []
    num_of_records = []
    # extract records by certain time_period
    records = data.values[data.values[:, 1] == time, :]
    for i in range(records.shape[0]):
        lat_axis.append((records[i, 0] // grid_nums) * grid_interval + lat_s)
        lon_axis.append((records[i, 0] % grid_nums) * grid_interval + lon_w)
        avg_speed.append(records[i, 2])
        num_of_records.append(records[i, 3])
    # save in np.array
    com = np.array([lon_axis, lat_axis, avg_speed, num_of_records]).reshape(4, -1)
    com = np.transpose(com)
    # save in DataFrame
    df = pd.DataFrame(com, columns=['lon', 'lat', 'speed', 'counts'])

    return df


# convert DataFrame to geojson dict
def df_to_geojson(df, properties, feature_type='Point'):
    """
    Turn a DataFrame containing point data into a geojson formatted python dictionary

    df : Pandas DataFrame
    properties : a list of columns in the DataFrame to turn into geojson feature properties
    latitude : df['lat']
    longitude : df['lon']
    FeatureType : Types for geometry. Possible options are Point, LineString, Polygon, \
                  MultiPoint, MultiLineString, and MultiPolygon. \
                  refer to http://geojson.org/
    Modified from https://github.com/gboeing/urban-data-science/...\
                  leaflet-simple-demo/pandas-to-geojson.ipynb
    """

    # dict to contain geojson data
    geojson = {'type': 'FeatureCollection', 'features': []}

    # convert each record in df using geojson format
    for idx, record in df.iterrows():
        # create a feature template
        feature = {'type': 'Feature',
                   'properties': {},
                   'geometry': {'type': feature_type,
                                'coordinates': []}}

        # fill in the coordinates
        feature['geometry']['coordinates'] = [record['lon'], record['lat']]

        # for each column, get the value and add it as a new feature property
        for prop in properties:
            feature['properties'][prop] = record[prop]

        # add this feature
        geojson['features'].append(feature)
    # convert geojson dict to str
    return geojson


if __name__ == "__main__":
    extract_records = data_by_time(0)
    test = extract_records.loc[0:10, :]
    geo_property = ['speed', 'counts']
    geojson = df_to_geojson(test, geo_property)
    print(type(geojson), ':')
    print(geojson)

