<template>
  <div>
    <div id="mapContainer"></div>
  </div>
</template>

<script>
import * as d3 from 'd3';
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
      const busMap = this.map;
      function projectPoint(x, y) {
        const point = busMap.latLngToLayerPoint(new L.LatLng(y, x));
        this.stream.point(point.x, point.y);
      }

      const transform = d3.geoTransform({ point: projectPoint });
      const path = d3.geoPath().projection(transform);

      this.$nextTick(() => {
        const features = this.pointContainer
          .selectAll('path')
          .data(this.busLocations.features)
          .enter()
          .append('path');

        features.attr('d', path);

        const bounds = path.bounds(this.busLocations);
        const topLeft = bounds[0];
        const bottomRight = bounds[1];

        this.svg.attr('width', bottomRight[0] - topLeft[0])
          .attr('height', bottomRight[1] - topLeft[1])
          .style('left', topLeft[0] + 'px')
          .style('top', topLeft[1] + 'px');

        this.pointContainer.attr('transform', 'translate(' + -topLeft[0] + ',' + -topLeft[1] + ')');
      });
    },
    drawBuses2() {
      L.svg().addTo(this.map);

      // Select the svg area and add circles:
      d3.select('#mapContainer')
        .select('svg')
        .selectAll('myCircles')
        .data(this.busLocations.features)
        .enter()
        .append('circle')
          .attr('cx', (d) => this.map.latLngToLayerPoint(d.geometry.coordinates).x)
          .attr('cy', (d) => this.map.latLngToLayerPoint(d.geometry.coordinates).y)
          .attr('r', 4)
          .style('fill', 'black')
          .attr('stroke', 'red')
          .attr('stroke-width', 3)
          .attr('fill-opacity', 0.8);

      // Function that update circle position if something change
      function update() {
        d3.selectAll('circle')
          .attr('cx', function (d) { return this.map.latLngToLayerPoint(d.coordinates).x; })
          .attr('cy', function (d) { return this.map.latLngToLayerPoint(d.coordinates).y; });
      }

      // If the user change the map (zoom or drag), I update circle position:
      this.map.on('moveend', update);
    },
    drawMap() {
      this.map = L.map('mapContainer').setView(this.center, 13);
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

    this.svg = d3.select(this.map.getPanes().overlayPane).append('svg');
    this.pointContainer = this.svg.append('g').attr('class', 'leaflet-zoom-hide');

    this.$nextTick(() => {
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
