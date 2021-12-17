
# %%
import re
import pandas as pd
import json

# %%
class DeploymentPlan() :
    def __init__(self, plan_name):
        self.plan_name = plan_name
        self.charging_stations = []

#%%
with open('./data_input/2. Deployment Plans/1. Solutions/p20.txt') as p20, open('./data_input/2. Deployment Plans/1. Solutions/p60.txt') as p60, open('./data_input/2. Deployment Plans/1. Solutions/p180.txt') as p180:
    p20_data = p20.readlines()
    p60_data = p60.readlines()
    p180_data = p180.readlines()

UTA_stops_df = pd.read_csv('./data_input/2. Deployment Plans/2. UTA_Runcut_Potential_Stop.csv', header=0)

# %%
def Extract_Plan_Data(raw_deployment_data, UTA_stops_df, plan_name):
    Z, m, X, Y = {}, {}, {}, {}
    converted_buses = []
    charging_stations = []
    total_charging_stations = 0
    total_miles = 0
    plan = DeploymentPlan(plan_name)

    #Process raw deployment data
    for i, line in enumerate(raw_deployment_data):
        if line[0] == '#':
            line_arr = line.split()
            plan.env_equity = round(float(line_arr[-1].strip()), 1)
        if line[0] == 'Z':
            Z_data = line[1:].strip().split(" ")
            Z[Z_data[0]] = int(Z_data[1])
        elif line[0] == 'm':
            m_data = re.split(' |_', line[1:].strip())      
            if m_data[1] == '0':
                m[m_data[0]] = []
            m[m_data[0]].append(float(m_data[2])) #Assumes that the list of stops will be in numerical order
        elif line[0] == 'Y':
            Y_data = line[1:].strip().split(" ")
            Y[Y_data[0]] = int(Y_data[1])

    for bus_id in Z.keys():
        if Z[bus_id] == 1:
            converted_buses.append(bus_id)
            if bus_id in m:
                daily_miles = 0
                for i, entry in enumerate(m[bus_id]):
                    if entry != 0:
                        daily_miles += (entry - m[bus_id][i-1])
                total_miles += daily_miles

    for stop_id in Y.keys():
        if Y[stop_id] > 0:
            total_charging_stations += Y[stop_id]
            stop_name = UTA_stops_df.loc[UTA_stops_df['stop_id'] == int(stop_id), 'stop_name'].iloc[0]
            plan.charging_stations.append({'stop_id': stop_id, 'stop_name': stop_name, 'num_stations': Y[stop_id]})
                
    plan.converted_buses = converted_buses
    plan.num_buses = len(converted_buses)
    plan.num_miles = round(total_miles, 1)
    plan.num_charging_stations = total_charging_stations

    return plan

# %%
plan_p20 = Extract_Plan_Data(p20_data, UTA_stops_df, 'p20')
plan_p60 = Extract_Plan_Data(p60_data, UTA_stops_df, 'p60')
plan_p180 = Extract_Plan_Data(p180_data, UTA_stops_df, 'p180')

plan_p20_json = json.dumps(plan_p20.__dict__)
plan_p60_json = json.dumps(plan_p60.__dict__)
plan_p180_json = json.dumps(plan_p180.__dict__)

p20_plan_data = open('./src/data/plans/p20.json', 'w')
p20_plan_data.write(plan_p20_json)
p20_plan_data.close()

p60_plan_data = open('./src/data/plans/p60.json', 'w')
p60_plan_data.write(plan_p60_json)
p60_plan_data.close()

p180_plan_data = open('./src/data/plans/p180.json', 'w')
p180_plan_data.write(plan_p180_json)
p180_plan_data.close()


    
        

