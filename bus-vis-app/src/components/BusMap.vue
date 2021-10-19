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
// import busStops from '../data/BusStops_UTA.json';

export default {
  name: 'BusMap',
  data() {
    return {
      center: [40.7608, -111.891],
      map: null,
      svg: null,
      pointContainer: null
    };
  },
  computed: {
    busLocations: function () {
      return this.$store.state.busLocations;
    },
  },
  watch: {
    busLocations: function () {
      this.drawBuses();
    }
  },
  methods: {
    drawBuses() {
      console.log(this.busLocations.features[0].geometry.coordinates);
      const geojsonMarkerOptions = {
        radius: 6,
        fillColor: '#ff7800',
        color: '#000',
        weight: 1,
        opacity: 1,
        fillOpacity: 0.8
      };
      L.geoJson(this.busLocations, { 
          pointToLayer: function (feature, latlng) {
          return L.circleMarker(latlng, geojsonMarkerOptions);
          }
       }).addTo(this.map);
    },
    drawMap() {
      this.map = L.map(this.$refs.mapElement).setView(this.center, 13);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      }).addTo(this.map);

      const routeStyle = {
        color: 'blue',
        opacity: 0.5,
        weight: 2,
      };
      L.geoJson(busRoutes, { style: routeStyle }).addTo(this.map);
    }
  },
  mounted() {
    this.drawMap();

    this.$nextTick(() => {
      console.log(this.busLocations.features[0]);
      this.drawBuses();
    });
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
