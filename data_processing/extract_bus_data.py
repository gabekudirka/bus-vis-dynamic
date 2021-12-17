# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import re
import pandas as pd
import json


# %%
class Bus:
    def __init__(self, bus_id):
        self.id = bus_id
        self.stops = []

# %%
with open('./data_input/2. Deployment Plans/1. Solutions/p20.txt') as p20, open('./data_input/2. Deployment Plans/1. Solutions/p60.txt') as p60, open('./data_input/2. Deployment Plans/1. Solutions/p180.txt') as p180:
    p20_data = p20.readlines()
    p60_data = p60.readlines()
    p180_data = p180.readlines()

#%%
UTA_runcut_df = pd.read_csv('./data_input/1. Network Data/3. UTA Runcut File  Aug2016.csv', header=0)
UTA_stops_df = pd.read_csv('./data_input/2. Deployment Plans/2. UTA_Runcut_Potential_Stop.csv', header=0)
bus_env_impact_df = pd.read_csv('./data_input/3. Supplementary Data/8. Ei_for_bus.csv', header=0)

#%%
def Extract_Bus_Data(raw_deployment_data, UTA_schedule_df, UTA_stops_df, env_impact_df):
    Z, m, X, Y = {}, {}, {}, {}
    new_stop_id = 135
    buses = []

    #Process raw deployment data
    for i, line in enumerate(raw_deployment_data):
        if line[0] == 'Z':
            Z_data = line[1:].strip().split(" ")
            Z[Z_data[0]] = int(Z_data[1])
        elif line[0] == 'm':
            m_data = re.split(' |_', line[1:].strip())      
            if m_data[1] == '0':
                m[m_data[0]] = []
            m[m_data[0]].append(float(m_data[2])) #Assumes that the list of stops will be in numerical order
        elif line[0] == 'X':
            X_data = re.split(' |_', line[1:].strip())      
            if X_data[1] == '1':
                X[X_data[0]] = []
            X[X_data[0]].append(int(X_data[2])) #Assumes that the list of stops will be in numerical order
        elif line[0] == 'Y':
            Y_data = line[1:].strip().split(" ")
            Y[Y_data[0]] = int(Y_data[1])
    
    #Build bus objects with all data sources
    for bus_id in Z.keys():
        bus = Bus(bus_id)
        bus.converted = Z[bus_id]
        bus_runcut_data = UTA_schedule_df.loc[UTA_schedule_df['block_num'] == int(bus_id)]
        bus.line = bus_runcut_data['LineAbbr'].iloc[0]
        bus.environmental_equity = round(float(env_impact_df.loc[env_impact_df['block_num'] == int(bus_id), 'Ei'].iloc[0]), 1)
        if bus_id in m:
            for i in range(len(bus_runcut_data) + 1):
                distance_traveled = m[bus_id][i]
                remaining_charge = 100 - (100 * (distance_traveled / 62))

                if i == 0:
                    stop_name = bus_runcut_data['from_stop'].iloc[i]
                    arrival_time = ''
                    departure_time = bus_runcut_data['FromTime'].iloc[i]
                    direction = bus_runcut_data['DirectionName'].iloc[i]
                    is_charging = 0
                else:
                    #For some buses there are more stops in the deployment plans then are listed in the runcut so I just treat the last stop in the
                    #runcut as the last stop and ignore the last in the deployment plan. This only affects non converted buses so it shouldn't matter
                    is_charging = X[bus_id][i-1]
                    stop_name = bus_runcut_data['to_stop'].iloc[i-1]
                    arrival_time = bus_runcut_data['ToTime'].iloc[i-1]
                    if i == len(bus_runcut_data):
                        departure_time = ''
                        direction = ''
                    else:
                        departure_time = bus_runcut_data['FromTime'].iloc[i]
                        direction = bus_runcut_data['DirectionName'].iloc[i]

                if stop_name in UTA_stops_df.values:
                    stop_id = UTA_stops_df.loc[UTA_stops_df['stop_name'] == stop_name,'stop_id'].iloc[0]
                else:
                    stop_id = new_stop_id
                    new_stop_id += 1

                stop_data = {
                    "stop_id": int(stop_id),
                    "stop_name": stop_name,
                    "arrival_time": arrival_time,
                    "departure_time": departure_time,
                    "direction": direction,
                    "distance_traveled": round(distance_traveled, 1),
                    "remaining_charge": round(remaining_charge, 1),
                    "is_charging": is_charging
                }
                bus.stops.append(stop_data)
            
        buses.append(bus.__dict__)

    return buses
# %%
buses_p20 = Extract_Bus_Data(p20_data, UTA_runcut_df, UTA_stops_df, bus_env_impact_df)
buses_p60 = Extract_Bus_Data(p60_data, UTA_runcut_df, UTA_stops_df, bus_env_impact_df)
buses_p180 = Extract_Bus_Data(p180_data, UTA_runcut_df, UTA_stops_df, bus_env_impact_df)

buses_p20_formatted = { "buses": buses_p20 }
buses_p60_formatted = { "buses": buses_p60 }
buses_p180_formatted = { "buses": buses_p180 }

buses_p20_json = json.dumps(buses_p20_formatted)
buses_p60_json = json.dumps(buses_p60_formatted)
buses_p180_json = json.dumps(buses_p180_formatted)

# %%
p20_bus_data = open('./src/data/buses/p20.json', 'w')
p20_bus_data.write(buses_p20_json)
p20_bus_data.close()

p60_bus_data = open('./src/data/buses/p60.json', 'w')
p60_bus_data.write(buses_p60_json)
p60_bus_data.close()

p180_bus_data = open('./src/data/buses/p180.json', 'w')
p180_bus_data.write(buses_p180_json)
p180_bus_data.close()