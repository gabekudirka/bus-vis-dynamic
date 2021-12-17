# %%
import csv
import json
import pandas as pd

# %%
f = open('src/data/supplementary_data/TAZ.json', 'r')
base_taz_regions = json.load(f)
f.close()

# %%
income_df = pd.read_csv('./data_input/3. Supplementary Data/Marginal_Income.csv')
household_df = pd.read_csv('./data_input/3. Supplementary Data/SE_File_v83_SE19_Net19.csv')


# %%
def get_income_bracket_percent(income_bracket):
    if income_bracket[5] == 0:
        return 0, 0, 0, 0, 0, 0
    else:
        return income_bracket[0], \
               round((income_bracket[1] / income_bracket[5]) * 100, 1), \
               round((income_bracket[2] / income_bracket[5]) * 100, 1), \
               round((income_bracket[3] / income_bracket[5]) * 100, 1), \
               round((income_bracket[4] / income_bracket[5]) * 100, 1), \
               round(income_bracket[5])
    
for feature in base_taz_regions['features']:
    taz = feature['properties']['N___CO_TAZ']
    taz_income_vals = income_df[income_df['CO_TAZID'] == taz].values[0]
    taz_income_vals = get_income_bracket_percent(taz_income_vals)
    taz_household_vals = household_df[household_df['CO_TAZID'] == taz].values[0]

    feature['properties']['inc_bracket1'] = taz_income_vals[1]
    feature['properties']['inc_bracket2'] = taz_income_vals[2]
    feature['properties']['inc_bracket3'] = taz_income_vals[3]
    feature['properties']['inc_bracket4'] = taz_income_vals[4]
    feature['properties']['total_households'] = taz_income_vals[5]

    feature['properties']['household_pop'] = taz_household_vals[2]
    feature['properties']['avg_size'] = taz_household_vals[3]
    feature['properties']['total_employment'] = taz_household_vals[4]


base_taz_regions_json = json.dumps(base_taz_regions)
with open('src/data/supplementary_data/taz_region_data.json', 'w') as f:
    f.write(base_taz_regions_json)