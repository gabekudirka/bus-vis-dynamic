# Electric Bus Visualization Setup:

## Create a directory inside of bus-vis-app called 'data_input'

## Move all of the electric bus data into data_input so that the file structure looks like this
## IMPORTANT: Due to difficulties handling excel files, '2. UTA_Runcut_Potential_Stop.xls' and
## '3. UTA Runcut File  Aug2016.xlsx' must be converted to csv files. To do this, open the xls/xlsx
## file in excel and save as a csv file.

```
data_input
│
└───1. Network Data
    │   3. UTA Runcut File  Aug2016.xlsx
│   │   3. UTA Runcut File  Aug2016.csv
│   │   metadata.txt
│   │
│   └───1. BusRoutes_UTA
│   │    │ BusRoutes_UTA.shp
│   │    │ BusRoutes_UTA.dbf
│   │    │ ...
│   │
│   └───2. BusStops_UTA
│        │ BusStops_UTA.shp
│        │ BusStops_UTA.dbf
│        │ ...    
│   
└───2. Deployment Plans
│    │   2. UTA_Runcut_Potential_Stop.xls
│    │   2. UTA_Runcut_Potential_Stop.csv
│    │   metadata.txt
│    │
│    └───1. Solutions  
│        │   p20.txt
│        │   p60.txt
│        │   p180.txt   
│
└───3. Supplementary Data
    │   5. Marginal_Income
    │   6. SE_File_v83_SE19_Net19 
    │   7. Pollutant Concentration.csv
    │   8. Ei_for_bus.scv  
    │
    └───4. TAZ
        │ TAZ.shp
        │ TAZ.dbf
        │ ...
```
## From the command prompt run the following script to install required packages
```
install_packages.bat
```

## On the command line run the following from the bus-vis-app directory to process the data and create the required directories (Ignore warnings in command line)
```
process_data.bat
```

## On the command line run the following from the bus-vis-app directory to set the coordinates of the region
## of interest and set the default zoom level of the map
```
set_city_coordinates.bat
```
## Run the app with the following command
```
npm run serve
```
## The app will now be running at localhost:8080