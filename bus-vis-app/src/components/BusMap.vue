<template>
 <div>
   <div id="mapContainer"></div>
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
            center: [40.7608, -111.8910],
            busMap: null,
        };
    },
    mounted() {
        this.busMap = L.map('mapContainer').setView(this.center, 13);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          maxZoom: 18,
          attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(this.busMap);

        const routeStyle = {
            color: 'blue',
            opacity: 0.5,
            weight: 2
        };
        L.geoJson(busRoutes, { style: routeStyle }).addTo(this.busMap);
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
  }
};

</script>

<style scoped>
#mapContainer {
    /* Not sure how to handle the height here */
    width: 100%;
    height: 70vh;
}
</style>
