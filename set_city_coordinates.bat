@echo off
set /p X="Enter X coordinate of city center: "
set /p Y="Enter Y coordinate of city center: "
set /p zoom="Enter default zoom level (12 is a good starting value): "

echo VUE_APP_COORDS_X=%X% > .env
echo VUE_APP_COORDS_Y=%Y% >> .env
echo VUE_APP_ZOOM=%zoom% >> .env