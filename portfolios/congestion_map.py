import pandas as pd
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def get_ref():
    file = BASE_DIR+'/static/data/majorRoads.geojson'
    with open(file, 'r') as f:
        geo_features = json.load(f)
        features = geo_features['features']
    """
    example record in features

        {
          "type": "Feature",
          "geometry": {
            "type": "MultiLineString",
            "coordinates": [[100.5733156, 13.7737855],
                            [100.5733266, 13.7739458]]
          },
          "properties": {
            "gid":167277,
          }
        }

    """
    ref = {}
    for feature in features:
        gid = feature['properties']['gid']
        coords = feature['geometry']["coordinates"]
        ref[str(int(gid))] = coords

    return ref


def data_by_time(time):
    # columns = [grid_id,time_id,speed,counts,gid]
    file = BASE_DIR+'/static/data/mapResult_500x.csv'
    datas = pd.read_csv(file)
    # initial parameters
    datas = datas[datas["time_id"] == time]
    records = []
    for idx, data in datas.iterrows():
        record = {str(int(data["gid"])):data["speed"]}
        records.append(record)
    return records


def df_to_geojson(df, refer):
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
                   'geometry': {'type': 'MultiLineString',
                                'coordinates': []}}

        # fill in the coordinates
        feature['geometry']['coordinates'] = refer[int(record['gid'])]

        # for each column, get the value and add it as a new feature property
        feature['properties']['speed'] = record['speed']
        # feature['properties']['gid'] = record['gid']
        # add this feature
        geojson['features'].append(feature)
    # convert geojson dict to str
    return geojson


if __name__ == "__main__":
    # records = data_by_time(32)
    refers = get_ref()
    records = data_by_time(0)
    print(type(refers), ':')

    print('length', len(records), records[0])
    print({'records':records})
