# Code Structure:
### Root Directory:
In the root directory all .bat files are for setting up the visualization with new data as explained below.
All other files serve as configuration files for the rest of the application. The code used to process new
data is stored in 'data_processing'. This code must be run before launching the application with new data.
The src directory contains all of the code for the application itself, including all visualizations.

### /Data Processing:
This directory contains all of the code used to process data for the application. 
'combine_taz_data.py' is used to extract data for the various TAZ regions in a given city so that they can be
added to overlays on the map.
'convert_pollutant_data.py' converts PM2.5 air quality data to json format so it can
be added to an overlay on the map. 
'extract_bus_data.py' takes in all of the bus data for a given transit system and extracts the necessary 
properties in the correct format to be used in the application.
'extract_plan_data.py' extracts the deployment plan data from each of the given plans and saves that to a new
file.
'wrangling.py' Takes in data from the bus routes, bus stops, and bus deployment plans and combines it with
the bus data so that it can all be visualized together.

### /src
This directory contains all of the code used in the application. All visualizations are performed with D3 and 
Leaflet and Vue is used to manage the application. The 'store' directory contains an index.js file which manages the 
state of the application using Vuex state management. The 'assets' directory contains all of the icons and images
used in the application. The 'components' directory contains all of the code for the application and visualizations.
App.vue sets the overall layout for the application and calls the necessary components. It also defines some of the
css classes used in the application. 

### /src/components
'BusMap.vue' loads the map, creates the overlays from the data, draws routes and stops, and draws the busses and charging
stations. All of interactions on the map like clicking on busses and routes are also handled in this file.
Whenever changes are made in other panels of the application like the time of day, selected bus, or deployment plan,
those changes are watched for in this file and are then reflected on the map.
'BusPanel.vue' loads in the data for a selected bus and displays it on the bottom panel. It also
calls the PanelChart component with the currently selected data to draw the graph visualizations.
'BussesList.vue' displays all of the busses in the data along with their bus number, line, environmental equity score
and current battery level. This component also implements the functionality for selecting busses from the list and
checking whether or not to view a certain bus from the list.
'HelpModal.vue' Creates the layout and displays the information on the help modal.
'ListContainer.vue' sets the layout for the left panel which includes the bus list, the help modal icon, the
station/bus toggle, and the 'show only converted bussees' checkbox.
'MapPanel.vue' is a container for the map section of the application including the time slider and the map itself. In this
component the locations of busses at a given time are also calcualted.
'PanelChart.vue' Takes in data from a bus or charging station and then plots it on a graph using D3.js. These charts
are used in the BusPanel component.
'PlanDetails.vue' creates the panel on the leftside of the page containing information about the selected deployment
plan. This component also allows the user to change the selected deployment plan.
'RoutesList.vue' is not currently used in the application
'RoutesItem.vue' is not currently used in the application
'StationPanel.vue' dloads the data for a selected charging station and dispalys it along with a graph on the bottom
panel.
'StationsList.vue' displays all of the charging stations created under the selected deployment in the left panel when
the stations/buses toggle is set to 'Stations'
'TimeSlider.vue' creates the time slider underneath the map and adds the functionality to update the time in the application
when the slider is moved.
'ToggleSwitch.vue' creates the bus/stations toggle on the leftside panel and its corresponding functionality.

### /src/store
This directory contains a file sets functions that allow individual components to update the state of the overall applicastion.
This allows for interactivity across panels like changing the deployment plan or updating the time of day.



# Electric Bus Visualization Setup:

### Create a directory inside of bus-vis-app called 'data_input'

### Move all of the electric bus data into data_input with the following file structure
***IMPORTANT***: Due to difficulties handling excel files, '2. UTA_Runcut_Potential_Stop.xls' and
3. UTA Runcut File  Aug2016.xlsx' must be converted to csv files. To do this, open the xls/xlsx
file in excel and save as a csv file.

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
### From the command prompt run the following script to install required packages
```
install_packages.bat
```

### On the command line run the following from the bus-vis-app directory to process the data and create the required directories (Ignore warnings in command line)
```
process_data.bat
```

### On the command line run the following from the bus-vis-app directory to set the coordinates of the region of interest and set the default zoom level of the map
```
set_city_coordinates.bat
```
### Run the app with the following command
```
npm run serve
```
### The app will now be running at localhost:8080