/* eslint-disable */
<template>
  <div>
    <div id="mapContainer" ref="mapElement">
  </div>
  </div>
</template>

<script>
import 'leaflet/dist/leaflet.css';
import 'leaflet-control-geocoder/dist/Control.Geocoder.css';
import L from 'leaflet';
import voronoi from '@turf/voronoi';
import bbox from '@turf/bbox';
import busRoutes from '../data/BusRoutes_UTA.json';
import greenBusIcon from '../assets/images/busIconGreen.png';
import busIcon from '../assets/images/busIcon.png';
import orangeIcon from '../assets/images/orange_icon2.png';
import chargingStationIcon from '../assets/images/chargingStation.png';
import busStops from '../data/BusStops_UTA.json';
import p20Stations from '../data/stationLocations/p20.json';
import p60Stations from '../data/stationLocations/p60.json';
import p180Stations from '../data/stationLocations/p180.json';
import tazRegions from '../data/supplementary_data/taz_region_data.json';
import pollutantConcentrations from '../data/supplementary_data/pollutant_concentrations.json';

export default {
  name: 'BusMap',
  data() {
    return {
      center: [process.env.VUE_APP_COORDS_X, process.env.VUE_APP_COORDS_Y],
      zoom: process.env.VUE_APP_ZOOM,
      map: null,
      busMarkers: null,
      stationMarkers: null,
      economicLegend: this.createLegend('economic'),
      pollutantLegend: this.createLegend('pollutant'),
      routeStyle: {
        color: 'blue',
        opacity: 0.5,
        weight: 2,
      },
      busStopStyle: {
        radius: 1,
        fillColor: 'black',
        color: '#000',
        weight: 1,
        opacity: 0.8,
        fillOpacity: 0.8
      },
      unclickedRouteStyle: {
        opacity: 0.65,
        weight: 3,
        color: 'blue',
      },
      clickedRouteStyle: {
        opacity: 0.8,
        weight: 4,
        color: 'red',
      },
      selectedBus: -1,
      selectedRoute: -1,
      selectedStation: -1,
      hoveredRoute: -1,
    };
  },
  computed: {
    busLocations: function () {
      return this.$store.state.busLocations;  
    },
    showBusPanel: function () {
      return this.$store.state.showBusses;
    },
    plan: function () {
      return this.$store.state.plan;
    },
    stateSelectedBus: function () {
      return this.$store.state.selectedBus;
    },
    stateSelectedStation: function () {
      return this.$store.state.selectedStation;
    },
    routeFocused: function () {
      return this.$store.state.routeFocused;
    },
    blackIcon: function () {
      return L.icon({
        iconUrl: busIcon,
        iconSize: [20, 20],
      });
    },
    greenIcon: function () {
      return L.icon({
        iconUrl: greenBusIcon,
        iconSize: [20, 20],
      });
    },
    blackIconHighlighted: function () {
      return L.icon({
        iconUrl: busIcon,
        iconSize: [30, 30],
      });
    },
    greenIconHighlighted: function () {
      return L.icon({
        iconUrl: greenBusIcon,
        iconSize: [30, 30],
      });
    },
    pollutantIcon: function () {
      return L.icon({
        iconUrl: orangeIcon,
        iconSize: [25, 25],
      });
    },
    stationPanelIcon: function () {
      return L.icon({
        iconUrl: chargingStationIcon,
        iconSize: [40, 40],
        class: 'station'
      });
    },
    stationPanelIconHighlighted: function () {
      return L.icon({
        iconUrl: chargingStationIcon,
        iconSize: [50, 50],
        class: 'station'
      });
    },
    info: function () {
      const info = L.control({ position: 'bottomleft' });
      info.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'info');
        return this._div;
      };
      info.show = function (layer) {
        if (layer.feature.properties.N___CO_TAZ) {
          this._div.innerHTML = '<p>TAZ ID: <b>' + layer.feature.properties.N___CO_TAZ + '</b> </p>';
        } else if (layer.feature.properties.PM25) {
          this._div.innerHTML = '<p>PM2.5_ATM_ug/m3: <b>' + layer.feature.properties.PM25 + '</b> </p>';
        }
      };
      info.hide = function () {
        this._div.innerHTML = '';
      };

      return info;
    },
  },
  watch: {
    busLocations: {
      handler: function () {
        if (this.busMarkers != null) {
          this.updateBusPositions();
        }
      },
      deep: true
    },
    plan: function () {
      this.stationMarkers.eachLayer((layer) => {
        this.map.removeLayer(layer);
      });
      this.selectedStation = -1;

      if (this.plan === 'p20') {
        this.drawStationPanels(p20Stations);
      } else if (this.plan === 'p60') {
        this.drawStationPanels(p60Stations);
      } else {
        this.drawStationPanels(p180Stations);
      }
    },
    stateSelectedBus: function () {
      if (this.busMarkers != null) {
        let selectedLayer = null;
        this.busMarkers.eachLayer((layer) => {
          if (this.busLocations.features[layer.bus].properties.id === this.stateSelectedBus) {
            selectedLayer = layer;
          }
        });
        if (selectedLayer != null) {
          this.highlightBus(selectedLayer, this);
        }
      }
    },
    stateSelectedStation: function () {
      if (this.stationMarkers != null) {
        let selectedLayer = null;
        this.stationMarkers.eachLayer((layer) => {
          if (this.busLocations.features[layer.bus].properties.id === this.stateSelectedBus) {
            selectedLayer = layer;
          }
        });
        if (selectedLayer != null) {
          this.highlightBus(selectedLayer, this);
        }
      }
    },
  },
  methods: {
    drawStationPanels(stationLocations) {
      const ref = this;
      function onEachFeature(feature, layer) {
        layer.setZIndexOffset(-100);
        layer.setOpacity(0.9);
        layer.bindTooltip(`<p><b>Station ID: </b> ${feature.properties.stop_id}</p>
                           <p><b>Stop Name: </b> ${feature.properties.stop_name}</p>
                           <p><b>Number of stations: </b>${feature.properties.num_stations}</p>`);
        layer.on({
            click: function () {
              ref.$store.dispatch('changeStation', feature.properties.stop_id);
              if (ref.showBusPanel) {
                ref.$store.dispatch('changeShowBusses', false);
              }
              ref.highlightStation(layer);
            }
        });
      }
      this.stationMarkers = L.geoJson(stationLocations, {
        pointToLayer: function (feature, latlng) {
            return L.marker(latlng, { icon: ref.stationPanelIcon });
        },
        onEachFeature: onEachFeature
      });

      this.stationMarkers.addTo(this.map);
    },
    highlightStation(layer) {
      if (this.selectedBus !== -1) {
        const oldBusLayer = this.busMarkers._layers[this.selectedBus];
        const oldBus = this.busLocations.features[oldBusLayer.bus];
        if (oldBus.properties.converted) {
          oldBusLayer.setIcon(this.greenIcon);
          oldBusLayer.setZIndexOffset(-50);
        } else {
          oldBusLayer.setIcon(this.blackIcon);
          oldBusLayer.setZIndexOffset(-50);
        }
        this.selectedBus = -1;
      }
      const layerId = layer._leaflet_id;
      if (this.selectedStation === -1) {
        // if no station is selected, highlight the station
        this.selectedStation = layerId;
        layer.setIcon(this.stationPanelIconHighlighted);
        layer.setZIndexOffset(50);
      } else {
        // if a station is selected, unhighlight the bus
        const oldLayer = this.stationMarkers._layers[this.selectedStation];
        oldLayer.setIcon(this.stationPanelIcon);
        oldLayer.setZIndexOffset(-50);
        if (layerId === this.selectedStation) {
          // if the selected station is clicked, unselect it
          this.selectedStation = -1;
        } else {
          // if another station is clicked, highlight it
          this.selectedStation = layerId;
          layer.setIcon(this.stationPanelIconHighlighted);
          layer.setZIndexOffset(50);
        }
      }
    },
    drawBuses() {
      const ref = this;      
      function onEachFeature(feature, layer) {
        layer.bindTooltip(`<p><b>Bus ID:</b> ${feature.properties.id}</p>
                           <p><b>Bus Route:</b> ${feature.properties.route}</p>
                           <p>${feature.properties.converted ? 'Converted' : 'Not converted'}</p>`);
        layer.on({
            click: function () {
              const bus = ref.busLocations.features[layer.bus];
              if (ref.stateSelectedBus === bus.properties.id) {
                ref.highlightBus(layer, ref);
              } else {
                ref.$store.dispatch('changeBus', bus.properties.id);
              }
              if (!ref.showBusPanel) {
                ref.$store.dispatch('changeShowBusses', true);
              }
            }
        });
      }
      this.busMarkers = L.geoJson(this.busLocations, { 
          pointToLayer: function (feature, latlng) {
            if (feature.properties.converted) {
              return L.marker(latlng, { icon: ref.greenIcon });
            }
            return L.marker(latlng, { icon: ref.blackIcon });
          },
          onEachFeature: onEachFeature,
       });

       let i = 0;
       this.busMarkers.eachLayer((layer) => {
         layer.bus = i;
         i++;
       });

       this.busMarkers.addTo(this.map);
    },
    highlightBus(layer) {
      if (this.selectedStation !== -1) {
        const oldStationLayer = this.stationMarkers._layers[this.selectedStation];
        oldStationLayer.setIcon(this.stationPanelIcon);
        oldStationLayer.setZIndexOffset(-50);
        this.selectedStation = -1;
      }

      const layerId = layer._leaflet_id;
      const bus = this.busLocations.features[layer.bus];
      if (this.selectedBus === -1) {
        // if no bus is selected, highlight the bus
        this.highlightBusHelper(layer, bus.properties.converted);
        this.selectedBus = layerId;
      } else {
        // if a bus is selected, unhighlight the bus
        const oldLayer = this.busMarkers._layers[this.selectedBus];
        const oldBus = this.busLocations.features[oldLayer.bus];
        if (oldBus.properties.converted) {
          oldLayer.setIcon(this.greenIcon);
          oldLayer.setZIndexOffset(-50);
        } else {
          oldLayer.setIcon(this.blackIcon);
          oldLayer.setZIndexOffset(-50);
        }
        if (layerId === this.selectedBus) {
          // if the selected bus is clicked, unselect it
          this.selectedBus = -1;
        } else {
          // if another bus is clicked, highlight it
          this.highlightBusHelper(layer, bus.properties.converted);
          this.selectedBus = layerId;
        }
      }
    },
    highlightBusHelper(layer, converted) {
      if (converted) {
        layer.setIcon(this.greenIconHighlighted); 
      } else {
        layer.setIcon(this.blackIconHighlighted);
      }
      layer.setZIndexOffset(50);
      if (!this.map.getBounds().contains(layer.getLatLng())) {
        this.map.panTo(layer.getLatLng());
      }
    },
    drawRoutes() {
      const ref = this;

      const routeRenderer = L.canvas({ padding: 0.3, tolerance: 7 });

      const tooltip = L.control({ position: 'bottomright' });
      tooltip.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'route-tooltip');
        return this._div;
      };
      tooltip.show = function (route) {
        this._div.innerHTML = (route ? `<p>Bus Route: <b>${route.properties.LineAbbr} - ${route.properties.LineName} </b> </p>` : '');
      };
      tooltip.removeFrom = function () {
        this._div.innerHTML = '';
      };
      tooltip.addTo(ref.map);

      function onEachFeature(feature, layer) {
        let isClicked = false;
        layer.on({
          click: function () {
            ref.showAllBuses();
            ref.highlightRoute(layer, tooltip);
            layer.bringToFront();
          },
          contextmenu: function (e) {
            if (!ref.routeFocused) {
              if (!isClicked) {
                layer.bringToBack();
                layer.fire('mouseout');
                tooltip.removeFrom();
              } else {
                layer.bringToBack();
                layer.fire('mouseover');
                tooltip.show(layer.feature);
              }
            }
          },
          mouseover: function () {
            if (!ref.routeFocused) {
              tooltip.show(layer.feature);
              layer.setStyle({
                opacity: 0.65,
                weight: 4,
                color: '#ff4278',
              });
              layer.bringToFront();
              isClicked = false;
            } 
          },
          mouseout: function () {
            if (!ref.routeFocused) {
              layer.setStyle(ref.unclickedRouteStyle);
              isClicked = true;
            }
          }
        });
      }
      const routesOverlay = L.geoJson(busRoutes, { 
        style: this.unclickedRouteStyle,  
        onEachFeature: onEachFeature,
        renderer: routeRenderer
      });
      return routesOverlay;
    },
    highlightRoute(layer, tooltip) {
      if (this.selectedRoute === -1) {
        this.selectedRoute = layer._leaflet_id;
        layer.setStyle(this.clickedRouteStyle);
        layer.bringToFront();
        tooltip.show(layer.feature);
        this.hideBusesOffRoute(layer);
        this.$store.dispatch('changeRouteFocused', true);
      } else {
        if (this.selectedRoute === layer._leaflet_id) {
          this.selectedRoute = -1;
          layer.setStyle(this.unclickedRouteStyle);
          // if multiple overlapping routes, select and delselct one to push it to the back
          this.showAllBuses(); 
          this.$store.dispatch('changeRouteFocused', false);
        } else {
          const oldLayer = this.routesOverlay._layers[this.selectedRoute];
          oldLayer.setStyle(this.unclickedRouteStyle);
          this.selectedRoute = layer._leaflet_id;
          layer.setStyle(this.clickedRouteStyle);
          layer.bringToFront();
          tooltip.show(layer.feature);
          this.showAllBuses();
          this.hideBusesOffRoute(layer);
        }
      }
    },
    showAllBuses() {
      const allBuses = [];
      this.busLocations.features.map(bus => {
          bus.properties.show = true;
          allBuses.push(bus.properties.id);
          return bus;
      });

      this.$store.dispatch('changeBussesToShow', allBuses);
    },
    hideBusesOffRoute(layer) {
      // Get the buses not on the route
      const otherBuses = this.busLocations.features.filter(bus => bus.properties.route !== layer.feature.properties.LineAbbr);
      const routeBuses = this.busLocations.features.filter(bus => bus.properties.route === layer.feature.properties.LineAbbr);

      otherBuses.map(bus => {
          bus.properties.show = false;
          return bus;
      });

      this.$store.dispatch('changeBussesToShow', routeBuses.map(bus => bus.properties.id));
    },
    drawMap() {
      const osmMap = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      });

      const googleSat = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
          subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
      });

     this.map = L.map(this.$refs.mapElement, {
        center: this.center,
        layers: [osmMap, googleSat],
        zoom: this.zoom,
        doubleClickZoom: false,
      });

      this.routesOverlay = this.drawRoutes();
      this.routesOverlay.addTo(this.map);

      const busStopStyle = this.busStopStyle;
      const busStopOverlay = L.geoJson(busStops, {
        pointToLayer: function (feature, latlng) {
          return L.circleMarker(latlng, busStopStyle);
        }
      });
      busStopOverlay.addTo(this.map);

      const pollutantConcentrationOverlay = this.drawPollutantConcentrationOverlay();

      const economicOverlay = this.drawTazOverlay();

      const overlays = {
        'Economic Data by Region': economicOverlay,
        'Pollutant Concentrations': pollutantConcentrationOverlay,
        'Bus Stops': busStopOverlay,  
        'Bus Routes': this.routesOverlay,
      };

      const baseMaps = {
        'Open Street Maps': osmMap,
        'Google Sattelite': googleSat,
      };

      L.control.layers(baseMaps, overlays).addTo(this.map);

      this.map.on('overlayadd', (e) => {
        if (e.name === 'Economic Data by Region') {
          this.economicLegend.addTo(this.map);
          this.info.addTo(this.map);
        } else if (e.name === 'Pollutant Concentrations') {
          this.pollutantLegend.addTo(this.map);
          this.info.addTo(this.map);
        }
      });
      this.map.on('overlayremove', (e) => {
        if (e.name === 'Economic Data by Region') {
          this.economicLegend.remove();
          if (!this.map.hasLayer(pollutantConcentrationOverlay)) {
            this.info.remove();
          }
        } else if (e.name === 'Pollutant Concentrations') {
          this.pollutantLegend.remove();
          if (!this.map.hasLayer(economicOverlay)) {
            this.info.remove();
          }
        }
      });
    },
    drawPollutantConcentrationOverlay() {
      const ref = this;

      const pollutantBbox = bbox(pollutantConcentrations);
      const pollutantsVoronoi = voronoi(pollutantConcentrations, { pollutantBbox });
      pollutantsVoronoi.features.forEach((feature, i) => {
        feature.properties.PM25 = pollutantConcentrations.features[i].properties.PM25;
      });

      const onEachFeature = function (feature, layer) {
        layer.on({
            mouseover: ref.highlightFeature,
            mouseout: function (e) {
              pollutantConcentrationOverlay.resetStyle(e.target);
              ref.info.hide();
            },
        });
      };

      function pollutantOverlayStyle(feature) {
        return {
          fillColor: ref.getColor([0, 5, 10, 15, 20, 25, 30, 35], feature.properties.PM25),  
          weight: 1,
          opacity: 0.6,
          color: 'black',
          fillOpacity: 0.5,
        };
      }
      
      const pollutantConcentrationOverlay = L.geoJson(pollutantsVoronoi, {
        style: pollutantOverlayStyle,
        onEachFeature: onEachFeature
      });

      return pollutantConcentrationOverlay;
    },
    getColor(range, bracket1, bracket2 = 0, totalHouseholds = 1) {
      if (totalHouseholds === 0) {
        return '#fffefa';
      }
        
      const b = parseFloat(bracket1) + parseFloat(bracket2);
      return b > range[7] ? '#800026'
            : b > range[6] ? '#BD0026'
            : b > range[5] ? '#E31A1C'
            : b > range[4] ? '#FC4E2A'
            : b > range[3] ? '#FD8D3C'
            : b > range[2] ? '#FEB24C'
            : b > range[1] ? '#FED976'
            : b > range[0] ? '#FFEDA0'
            : '#fff7d6';
    },
    highlightFeature(e) {
      const layer = e.target;
      layer.setStyle({
          weight: 3,
          color: '#666',
          dashArray: '',
          fillOpacity: 0.7
      });

      if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
          layer.bringToFront();
      }

      this.info.show(layer); 
    },
    drawTazOverlay() {
      const ref = this;

      function displayTazInfo(props) {
        ref.info._div.innerHTML = '<p>TAZ ID: <b>' + props.target.feature.properties.N___CO_TAZ + '</b> </p>'
            + '<i>Households making:</i>'
            + '<br/> $0-$34k per year: &nbsp&nbsp&nbsp&nbsp<b>' + props.target.feature.properties.inc_bracket1
            + '%</b><br/> $35k-$50k per year: <b>' + props.target.feature.properties.inc_bracket2
            + '%</b><br/> $50k-$99k per year: <b>' + props.target.feature.properties.inc_bracket3
            + '%</b><br/> $100k+ per year: &nbsp&nbsp&nbsp&nbsp&nbsp<b>' + props.target.feature.properties.inc_bracket4
            + '%</b><br/> Total number of households: <b>' + props.target.feature.properties.total_households + '</b>';
      }

      function onEachFeature(feature, layer) {
        layer.on({
            mouseover: ref.highlightFeature,
            mouseout: function (e) {
              economicOverlay.resetStyle(e.target);
              ref.info.hide();
            },
            click: displayTazInfo
        });
      }

      function tazOverlayStyle(feature) {
        return {
          fillColor: ref.getColor([0, 10, 20, 30, 40, 50, 60, 70], feature.properties.inc_bracket1, feature.properties.inc_bracket2, feature.properties.total_households),  
          weight: 1,
          opacity: 0.6,
          color: 'black',
          fillOpacity: 0.5,
        };
      }

      const economicOverlay = L.geoJson(tazRegions, {
        style: tazOverlayStyle,
        onEachFeature: onEachFeature
      });

      return economicOverlay;
    },
    createLegend(overlayType) {
      const ref = this;
      const legend = L.control({ position: 'bottomleft' });

      legend.onAdd = function (map) {
          const div = L.DomUtil.create('div', 'info legend');

          if (overlayType === 'economic') {
            const grades = [0, 10, 20, 30, 40, 50, 60, 70]; 
            div.innerHTML = '<p><b>Households making </br> less than $50,000</b></p>';
            for (let i = 0; i < grades.length; i++) {
                div.innerHTML += '<i style="background:' + ref.getColor(grades, grades[i] + 1) + '"></i> '
                    + grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '%<br>' : '%+');
            }
            return div;
          } else if (overlayType === 'pollutant') {
            const grades = [0, 5, 10, 15, 20, 25, 30, 35]; 
            div.innerHTML = '<p><b>PM2.5 Levels</b></p>';
            for (let i = 0; i < grades.length; i++) {
                div.innerHTML += '<i style="background:' + ref.getColor(grades, grades[i] + 1) + '"></i> '
                    + grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
            }
            return div;
          }
      };
      return legend;
    },
    updateBusPositions() {
      this.busMarkers.eachLayer((layer) => {
        const bus = this.busLocations.features[layer.bus];
        if (!bus.properties.show && this.map.hasLayer(layer)) {
          this.map.removeLayer(layer);
        } else if (bus.properties.show) {
          if (!this.map.hasLayer(layer)) {
            this.map.addLayer(layer);
          }
          layer.bindTooltip(`<p><b>Bus ID:</b> ${bus.properties.id}</p>
                           <p><b>Bus Route:</b> ${bus.properties.route}</p>
                           <p>${bus.properties.converted ? 'Converted' : 'Not converted'}</p>`);
          const coords = bus.geometry.coordinates;
          if (layer._latlng.lng !== coords[0] || layer._latlng.lat !== coords[1]) {
            layer.setLatLng([coords[1], coords[0]]);
          }
          if (bus.properties.converted) {
            layer.setIcon(this.greenIcon);
          } else {
            layer.setIcon(this.blackIcon);
          }
        }
      });
    },
  },
  mounted() {
    this.drawMap();

    this.$nextTick(() => {
      this.drawStationPanels(p20Stations);
      this.drawBuses();
    });
  },
  beforeUnmount() {
    if (this.map) {
      this.map.remove();
    }
  },
};
</script>

<style scoped>
#mapContainer {
  min-height: 57vh;
  background-color: #fff;
  margin: .25em;
  padding: .25em;
  filter: drop-shadow(1px 1px 3px #dfdfdf);
  flex:5;
}

@media (max-height: 550px) {
  #mapContainer {
    min-height: 54vh;
  }
}
@media (max-height: 400px) {
  #mapContainer {
    min-height: 45vh;
  }
}
#mapContainer >>> .info {  
  padding: 6px 8px;
  font: 14px/16px Arial, Helvetica, sans-serif;
  border-radius: 5px;
  text-align: left;
  background: #fff;
}
#mapContainer >>> .info h2 {
  margin: 0 0 5px;
  color: #777;
}

#mapContainer >>> .route-tooltip {  
  padding: 4px 4px;
  background: white;
  border-radius: 5px;
  text-align: left;
}

#mapContainer >>> .leaflet-control-layers-base {  
  text-align: left; 
}

#mapContainer >>> .leaflet-control-layers-overlays {  
  text-align: left; 
}

#mapContainer >>> .legend {
    line-height: 18px;
    color: #555;
    background: #fff;
}

#mapContainer >>> .legend i {
    width: 18px;
    height: 18px;
    float: left;
    margin-right: 8px;
    opacity: 0.7;
}
</style>
