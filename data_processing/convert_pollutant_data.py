import csv, json
from geojson import Feature, FeatureCollection, Point

features = []
with open('./data_input/3. Supplementary Data/7. Pollutant Concentration.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for latitude, longitude, pm25 in reader:
        try:
            latitude, longitude = map(float, (latitude, longitude))
        except:
            continue
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