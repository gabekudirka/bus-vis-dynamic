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
// import busStops from '../data/BusStops_UTA.json';

export default {
  name: 'BusMap',
  data() {
    return {
      center: [40.7608, -111.891],
      map: null,
      busMarkers: null,
    };
  },
  computed: {
    busLocations: function () {
      return this.$store.state.busLocations;  
    },
    showBusPanel: function () {
      return this.$store.state.showBusses;
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
    routeStyle: function () {
      return {
        color: 'blue',
        opacity: 0.5,
        weight: 2,
      };
    }
  },
  watch: {
    busLocations: function () {
      if (this.busMarkers != null) {
        this.updateBusPositions();
      }
    }
  },
  methods: {
    drawBuses() {
      const ref = this;      
      function onEachFeature(feature, layer) {
        layer.bindTooltip(`<p><b>Bus ID:</b> ${feature.properties.id}</p>
                           <p><b>Bus Route:</b> ${feature.properties.route}</p>
                           <p>${feature.properties.converted ? 'Converted' : 'Not converted'}</p>`);
        layer.on({
            click: function () {
              ref.selectedIcon = layer;
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
      this.map = L.map(this.$refs.mapElement).setView(this.center, 13);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      }).addTo(this.map);

      L.geoJson(busRoutes, { style: this.routeStyle }).addTo(this.map);
    },
    updateBusPositions() {
      let i = 0;
      this.busMarkers.eachLayer((layer) => {
        const coords = this.busLocations.features[i].geometry.coordinates;
        if (layer._latlng.lng !== coords[0] || layer._latlng.lat !== coords[1]) {
          layer.setLatLng([coords[1], coords[0]]);
          i++;
        }
        if (this.busLocations.features[i].properties.converted) {
          layer.setIcon(this.greenIcon);
        } else {
          layer.setIcon(this.blackIcon);
        }
      });
    },
  },
  mounted() {
    this.drawMap();

    this.$nextTick(() => {
      this.drawBuses();
    });
    // DRAW BUS STOPS?
    // const geojsonMarkerOptions = {
    //     radius: 1,
    //     fillColor: 'red',
    //     color: '#000',
    //     weight: 1,
    //     opacity: 0.8,
    //     fillOpacity: 0.8
    // };

    // L.geoJson(busStops, {
    //     pointToLayer: function (feature, latlng) {
    //         return L.circleMarker(latlng, geojsonMarkerOptions);
    //     }
    // }).addTo(this.busMap);
  },
  beforeUnmount() {
    if (this.busMap) {
      this.busMap.remove();
    }
  },
};
</script>

<style scoped>
#mapContainer {
  /* Not sure how to handle the height here */
  width: 60vw;
  height: 75vh;
}
</style>
