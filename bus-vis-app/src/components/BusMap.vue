/* eslint-disable */
<template>
  <div>
    <div id="mapContainer" ref="mapElement"></div>
  </div>
</template>

<script>
import 'leaflet/dist/leaflet.css';
import 'leaflet-control-geocoder/dist/Control.Geocoder.css';
import L from 'leaflet';
import busRoutes from '../data/BusRoutes_UTA.json';
import greenBusIcon from '../assets/images/busIconGreen.png';
import busIcon from '../assets/images/busIcon.png';
import chargingStationIcon from '../assets/images/chargingStation.png';
import busStops from '../data/BusStops_UTA.json';
import p20Stations from '../data/stationLocations/p20.json';
import p60Stations from '../data/stationLocations/p60.json';
import p180Stations from '../data/stationLocations/p180.json';
import tazRegions from '../data/TAZ_with_data2.json';

export default {
  name: 'BusMap',
  data() {
    return {
      center: [40.7608, -111.891],
      map: null,
      busMarkers: null,
      stationMarkers: null,
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
      }
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
    stationPanelIcon: function () {
      return L.icon({
        iconUrl: chargingStationIcon,
        iconSize: [40, 40],
        class: 'station'
      });
    }
  },
  watch: {
    busLocations: function () {
      if (this.busMarkers != null) {
        this.updateBusPositions();
      }
    },
    plan: function () {
      this.stationMarkers.eachLayer((layer) => {
        this.map.removeLayer(layer);
      });

      if (this.plan === 'p20') {
        this.drawStationPanels(p20Stations);
        this.updateBusPositions();
      } else if (this.plan === 'p60') {
        this.drawStationPanels(p60Stations);
        this.updateBusPositions();
      } else {
        this.drawStationPanels(p180Stations);
        this.updateBusPositions();
      }
    }
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
    drawBuses() {
      const ref = this;      
      function onEachFeature(feature, layer) {
        layer.bindTooltip(`<p><b>Bus ID:</b> ${feature.properties.id}</p>
                           <p><b>Bus Route:</b> ${feature.properties.route}</p>
                           <p>${feature.properties.converted ? 'Converted' : 'Not converted'}</p>`);
        layer.on({
            click: function () {
              ref.$store.dispatch('changeBus', feature.properties.id);
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
          onEachFeature: onEachFeature
       });

       this.busMarkers.addTo(this.map);
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
        zoom: 13,
      });

      const routesOverlay = L.geoJson(busRoutes, { style: this.routeStyle });
      routesOverlay.addTo(this.map);

      const busStopStyle = this.busStopStyle;

      const busStopOverlay = L.geoJson(busStops, {
        pointToLayer: function (feature, latlng) {
          return L.circleMarker(latlng, busStopStyle);
        }
      });
      busStopOverlay.addTo(this.map);

      const info = L.control();

      function getColor(bracket1, bracket2, totalHouseholds) {
        if (totalHouseholds === 0) {
          return '#fffefa';
        }
          
        const b = parseFloat(bracket1) + parseFloat(bracket2);
        return b > 70 ? '#800026'
              : b > 60 ? '#BD0026'
              : b > 50 ? '#E31A1C'
              : b > 40 ? '#FC4E2A'
              : b > 30 ? '#FD8D3C'
              : b > 20 ? '#FEB24C'
              : b > 10 ? '#FED976'
              : b > 0 ? '#FFEDA0'
              : '#fff7d6';
      }

      function tazOverlayStyle(feature) {
        return {
            fillColor: getColor(feature.properties.inc_bracket1, feature.properties.inc_bracket2, feature.properties.total_households),  
            weight: 2,
            opacity: 0.6,
            color: 'black',
            dashArray: '3',
            fillOpacity: 0.5,
        };
      }

      function onEachFeature(feature, layer) {
        layer.on({
            mouseover: highlightFeature,
            mouseout: resetHighlight,
            click: zoomToFeature
        });
      }

      const overlayGeojson = L.geoJson(tazRegions, {
        style: tazOverlayStyle,
        onEachFeature: onEachFeature
      });

      function highlightFeature(e) {
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

        info.update(layer.feature.properties);
      }

      function resetHighlight(e) {
        overlayGeojson.resetStyle(e.target);
        info.update();
      }

      function zoomToFeature(e) {
        this.map.fitBounds(e.target.getBounds());
      }

      info.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'info');
        this.update();
        return this._div;
      };

      info.update = function (props) {
        this._div.innerHTML = (props ? '<h4>TAZ Code: <b>' + props.N___CO_TAZ + '</b> </h4>' 
            + 'Area: ' + props.AREA
            + '<br/> Households with income between $0-$34,999: ' + props.inc_bracket1
            + '%<br/> Households with income between $35,000-$49,999: ' + props.inc_bracket2
            + '%<br/> Households with income between $50,000-$99,999: ' + props.inc_bracket3
            + '%<br/> Households with income over $100,000: ' + props.inc_bracket4
            + '%<br/> Total number of households: ' + props.total_households : '');
      };

      info.addTo(this.map);

      const overlays = {
        'Economic Data by Region': overlayGeojson,
        'Bus Stops': busStopOverlay,  
        'Bus Routes': routesOverlay,
      };

      const baseMaps = {
        'Open Street Maps': osmMap,
        'Google Sattelite': googleSat,
      };

      L.control.layers(baseMaps, overlays).addTo(this.map);
    },
    updateBusPositions() {
      let i = 0;
      this.busMarkers.eachLayer((layer) => {
        const bus = this.busLocations.features[i];
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
        i++;
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
  background: white;
  background: rgba(255,255,255,0.8);
  box-shadow: 0 0 15px rgba(0,0,0,0.2);
  border-radius: 5px;
  text-align: left;
}
#mapContainer >>> .info h4 {
  margin: 0 0 5px;
  color: #777;
}
#mapContainer >>> .leaflet-control-layers-base {  
  text-align: left; 
}

#mapContainer >>> .leaflet-control-layers-overlays {  
  text-align: left; 
}
</style>
