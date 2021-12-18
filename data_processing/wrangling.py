import json
import openpyxl
import datetime
import itertools

datafolder = "data_input"

#output data file paths
allRoutes = 'src/data/allRoutes.json'
allStops = 'src/data/allStops.json'
busesAtStations = 'src/data/BusesAtStations.json'

routes = []

#read in route info and coordinates
data = json.load(open("src\\data\\BusRoutes_UTA.json"))
for r in data['features']:
    record = r["properties"]
    routes.append(
        {  
            'lineAbbr': record['LineAbbr'], 
            'lineName': record["LineName"], 
            'service': record["Service"], 
            'shape_length': record["Shape_Leng"], 
            'busses': set(),
            'coordinates': r['geometry']['coordinates']
        })

#calc length of each route
import math
for r in routes:
    for i in range(len(r['coordinates'])):
        sumdist = 0
        #calc dist between points 
        dist0 = r['coordinates'][i][0][0] - r['coordinates'][i - 1][0][0]
        dist1 = r['coordinates'][i][0][1] - r['coordinates'][i - 1][0][1]

        dist0 = r['coordinates'][i - 1][0][0] - r['coordinates'][i][0][0]
        dist1 = r['coordinates'][i - 1][0][1] - r['coordinates'][i][0][1]
        #sum of total distance
        sumdist += math.sqrt(dist0 * dist0 + dist1 * dist1)
    r['path_length'] = sumdist

#import list of busses from runcut

wb_obj = openpyxl.load_workbook(datafolder + "\\1. Network Data\\3. UTA Runcut File  Aug2016.xlsx")
sheet = wb_obj.active

i = 0
for row in sheet.iter_rows():
    i += 1
    if i == 1:
        continue
    for route in routes:
        if route['lineAbbr'] == row[0].value:
            route['busses'].add(row[3].value)

#to write sets to json
def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

#write route array to allRoutes.json
with open(allRoutes, 'w') as outfile:
    json.dump(routes, outfile, default=set_default)

stops = []
data = json.load(open("src\\data\\BusStops_UTA.json"))
i = 0
for record in data["features"]:
    props = record["properties"]
    stops.append({
        'stopId' : props['StopId'],
        'stopName': props["StopName"],
        'streetNum': props["StreetNum"],
        'onStreet': props["OnStreet"],
        'atStreet': props["AtStreet"],
        'city': props["City"],
        'inService': props["InService"],
        'bench': props["Bench"],
        'shelter': props["Shelter"],
        'lighting': props["Lighting"],
        'garbage': props["Garbage"],
        'bicycle': props["Bicycle"],
        'transfer': props["Transfer"],
        'locationUs': props["LocationUs"],
        'UTAStopID': props["UTAStopID"],

        'coordinates': record['geometry']['coordinates']
    })
print("found", len(stops), "stops")

#write to allStops
with open(allStops, 'w') as outfile:
    json.dump(stops, outfile)

stations = {}
dataStations = json.load(open(allStops))

#put buses in locations by hour
for station in dataStations:
    stations[station['stopName']] = {'stop_id': station['stopId'], 'stop_name': station['stopName'], 'busTimes': {}}
planNames = ['p20', 'p60', 'p180']
#This depends on and adds to on our pre-written plan files
for plan in planNames:
    #find and write bus stop locations
    data = json.load(open("src\\data\\plans\\" + plan + ".json"))
    stops = json.load(open(allStops))
    finalFile = "src\\data\\stationLocations\\" + plan + ".json"
    statLocs = {'type': 'FeatureCollection', 'features': []}
    for cs in data['charging_stations']:
        coords = []
        # find allstopps where name matches
        for s in stops:
            if s["stopName"].replace(" ", "") == cs["stop_name"].replace(" ", ""):
                coords = s["coordinates"]
        if coords == []:
            print("NO COORDS", cs)
        geo = {'type': 'Point', 'coordinates': coords}
        ob = {'type': 'Feature', 'geometry': geo, 'properties': cs}
        statLocs['features'].append(ob)
    #write bus stop locations
    with open(finalFile, 'w') as outfile:
        json.dump(statLocs, outfile)

    dataBuses = json.load(open("src\\data\\buses\\" + plan + ".json"))
    for i in range(24):
        timeStr = str(i) + ":00"
        time = datetime.time(i)
        for bus in dataBuses['buses']:
            for stp in bus['stops']:
                arvtime = datetime.time(0) if (stp['arrival_time'] == '') else datetime.time(int(stp['arrival_time'].split(":")[0]), int(stp['arrival_time'].split(":")[1]))
                deptime = datetime.time(23,59) if (stp['departure_time'] == '') else datetime.time(int(stp['departure_time'].split(":")[0]), int(stp['departure_time'].split(":")[1]))
                if arvtime <= time and time <= deptime: #at stop
                    if stp['stop_name'] not in stations:
                        stations[stp['stop_name']] = {'stop_id': stp['stop_id'], 'stop_name': stp['stop_name'], 'busTimes': {}}
                    if timeStr not in stations[stp['stop_name']]['busTimes']:
                        stations[stp['stop_name']]['busTimes'][timeStr] = []
                    stations[stp['stop_name']]['busTimes'][timeStr].append(bus['id'])

#write em
with open(busesAtStations, 'w') as outfile:
    json.dump(stations, outfile)

#route sort! Takes in a list of coordinates and sorts them into a connected list
def sortRoutePath(rt):
    coords = rt['coordinates']
    head = rt['coordinates'][0][0] #start at the beginning. Could be anywhere tho
    tail = rt['coordinates'][0][1]
    lsts = [ [rt['coordinates'][0]] ]
    del coords[0]
    i = 0
    noneFound = False
    while len(coords):
        if noneFound: #can't add any more to that list, start a new one with new seed
            i += 1
            r = 0 #random.randrange(0, len(coords))
            lsts.append([coords[r]])
            head = coords[r][0]
            tail = coords[r][1]
            del coords[r]
        for c in coords: #find new head or tail
            noneFound = True
            if c[1] == head:
                lsts[i].insert(0, c)
                head = c[0]
                coords.remove(c)
                noneFound = False
                break
            elif c[0] == tail:
                lsts[i].append(c)
                tail = c[1]
                coords.remove(c)
                noneFound = False
                break

    #See if we can combine any of the lists
    #**This is where we should apply nearest neighbor
    for l1 in lsts: 
        for l2 in lsts:
            if l1 == l2:
                continue
            elif l1[0][0] == l2[-1][1]:
                l1 = l2 + l1
            elif l1[-1][1] == l2[0][0]:
                l1 = l1 + l2
            
    #otherwise just concat and hope there was some reason for the order they gave us these points in
    all = list(itertools.chain.from_iterable(lsts))
    return all

#sort the coordinates into one path (as close as we can with stupid data)
routes = json.load(open(allRoutes))
for rt in routes:
    rt['coordinates'] = sortRoutePath(rt)
print("sorted", len(routes), "routes")

#write it
with open(allRoutes, 'w') as outfile:
    json.dump(routes, outfile)
    