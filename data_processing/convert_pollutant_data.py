import csv, json
from geojson import Feature, FeatureCollection, Point
import pandas as pd

features = []
pollutant_df = pd.read_excel('./data_input/3. Supplementary Data/7. Pollutant Concentration.xlsx')
for index, row in pollutant_df.iterrows():
    latitude = row['lat']
    longitude = row['lon']
    pm25 = row['PM2.5_ATM_ug/m3']
    features.append(
            Feature(
                geometry = Point((longitude, latitude)),
                properties = {
                    'PM25': pm25,
                }
            )
        )
        
collection = FeatureCollection(features)
with open("src/data/supplementary_data/pollutant_concentrations.json", "w") as f:
    f.write('%s' % collection)