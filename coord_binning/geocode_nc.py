#!/usr/bin/python3

import geopandas as gp
import pandas as pd
import argparse

'''Code takes latitude and longitude coordinates along with path to shapefile
   and returns a neighborhood council identifier in response. Can be run as
   executable from command line or imported into another codebase as the
   classify_point function and run.

   SHAPEFILE: http://geohub.lacity.org/datasets/674f80b8edee4bf48551512896a1821d_0/data

   USE: python3 geocode_nc.py -lat 34.040871 -long -118.235202 -shp shp/ '''

parser = argparse.ArgumentParser(description='Assign a point within Los Angeles to a neighborhood council using a shapefile boundary')
parser.add_argument('-lat', '--latitude', type=float,
                    help='latitude coordinate value')
parser.add_argument('-long', '--longitude', type=float,
                    help='longitude coordinate value')
parser.add_argument('-shp', '--shapefile',
                    help='path to shapefile directory')
args = parser.parse_args()


def load_coords(latitude, longitude):
    # load coordinates as geopandas dataframe
    df = pd.DataFrame([{'name': 'POINT', 'lat': latitude, 'long': longitude}])
    gp_coord = gp.GeoDataFrame(df, geometry=gp.points_from_xy(df.long, df.lat))
    gp_coord.crs = "epsg:4326"
    return gp_coord


def load_shapefile(file_path):
    # load shapefile
    gp_shape = gp.read_file(file_path)
    gp_shape.crs = "epsg:4326"  # This is true for NC shapefile
    return gp_shape


def classify_point(latitude, longitude, shapefile_path):
    # perform join between coords and shapefile
    pt = load_coords(latitude, longitude)
    shp = load_shapefile(shapefile_path)
    joined_shp = gp.sjoin(pt, shp, how='left', op='intersects')
    nc = joined_shp.Name[0]
    # Return point classification
    if nc != nc:  # Check if returned value is nan
        return 'Point outside Los Angeles County'
    else:
        return nc


if __name__ == '__main__':
    nc = classify_point(latitude=args.latitude,
                        longitude=args.longitude,
                        shapefile_path=args.shapefile)
    print(nc)
