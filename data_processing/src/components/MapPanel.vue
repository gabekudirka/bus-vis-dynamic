/* eslint-disable max-len no-continue */
<template>
    <div>
        <div class="map">
            <BusMap /> 
        </div>
        <div class="time-slider">
            <TimeSlider />
        </div>
    </div>
</template>

<script>
import stopsList from '../data/allStops.json';
import routesList from '../data/allRoutes.json';
import TimeSlider from './TimeSlider.vue';
import BusMap from './BusMap.vue';

export default {
    name: 'MapPanel',
    components: {
        TimeSlider,
        BusMap
    },
    props: {
        planObj: {
            type: Object
        },
    },
    computed: {
        time: function () {
            return this.$store.state.time;
        },
        // returns array of {busID: ID, coordinates: [lat,long]}
        busLocations: function () { 
            return this.$store.state.busLocations;
        }
    },
    watch: {
        // update bus locations in state when time is changed
        time: function () {
            const busLocs = this.calcBusLocations();
            this.$store.dispatch('changeBusLocations', busLocs);
        },
        planObj: function () {
            const busLocs = this.calcBusLocations();
            this.$store.dispatch('changeBusLocations', busLocs);
        }
    },
    mounted: function () {
        const busLocs = this.calcBusLocations();
        this.$store.dispatch('changeBusLocations', busLocs);
    },
    methods: {
        geoJsonObj(busId, busCoordinates, converted, line, remainingCharge, atStation = false) {
            return { 
                type: 'Feature',
                properties: { 
                    id: busId,
                    converted: converted,
                    route: line,
                    atStation: atStation,
                    remainingCharge: remainingCharge,
                    show: (this.$store.state.busLocations.features.length > 1) ? this.$store.state.busLocations.features.find((bus) => bus.properties.id === busId).properties.show : true
                },
                geometry: {
                    type: 'Point',
                    coordinates: busCoordinates
                }
            };
        },
        calcBusLocations() {
            const dtstr = '1/1/2000'; // we change time strings into dates to take care of the arithmatic
            const curTime = new Date(dtstr + ' ' + this.time);
            const busLocs = {};
            busLocs.type = 'FeatureCollection';
            busLocs.features = [];
            this.planObj.buses.forEach((bus) => {
                for (let i = 0; i < bus.stops.length; i++) {                
                    const stp = bus.stops[i];
                    const arvtime = (stp.arrival_time === '') ? new Date(dtstr + ' 00:00') : new Date(dtstr + ' ' + stp.arrival_time);
                    const deptime = (stp.departure_time === '') ? new Date(dtstr + ' 23:59') : new Date(dtstr + ' ' + stp.departure_time);
                    const nextArvtime = (i < bus.stops.length - 1) ? new Date(dtstr + ' ' + bus.stops[i + 1].arrival_time) : new Date(dtstr + ' 00:00');
                    // if (bus.id !== '1000' && bus.id !== '1009') {
                    //     continue; // FOR DEBUGGING
                    // }

                    // if arv <= t <= dpt   -> at stop
                    if (arvtime <= curTime && curTime <= deptime) {
                        const stationObj = stopsList.find((station) => station.stopName === stp.stop_name);
                        
                        if (stationObj) {
                            busLocs.features.push(this.geoJsonObj(bus.id, stationObj.coordinates, bus.converted, bus.line, stp.remaining_charge, true));
                            break;
                        } else {
                            busLocs.features.push(this.geoJsonObj(bus.id, [0, 0], bus.converted, bus.line, stp.remaining_charge, true));
                            break;
                        }
                    // if dpt <= t <= next.arv   -> between stops.
                    // TODO: This is where we calculate between coordinates
                    } else if (deptime <= curTime && curTime <= nextArvtime) {
                        // calc coords
                        const coords = this.calcBusCoords(stp, bus.stops[i + 1], bus.line);
                        // console.log('Here2', coords, stp);
                        if (coords !== '') {
                            busLocs.features.push(this.geoJsonObj(bus.id, coords, bus.converted, bus.line, stp.remaining_charge));
                            break;
                        } else {
                            busLocs.features.push(this.geoJsonObj(bus.id, [0, 0], bus.converted, bus.line, stp.remaining_charge));
                            break;
                        }
                    // t <= arv   -> usually means bus has not left the station for the day        
                    } else if (curTime <= arvtime) {
                        // console.log('Here3', stp);
                        const stationObj = stopsList.find((station) => station.stopName === stp.stop_name);
                        if (stationObj) {
                            busLocs.features.push(this.geoJsonObj(bus.id, stationObj.coordinates, bus.converted, bus.line, stp.remaining_charge));
                            break;
                        } else {
                            busLocs.features.push(this.geoJsonObj(bus.id, [0, 0], bus.converted, bus.line, stp.remaining_charge));
                            break;
                        }
                    } 
                }
            });
            return busLocs;
        },
        calcDistBetwPts(pt1, pt2) {
            const dist0 = pt1[0] - pt2[0];
            const dist1 = pt1[1] - pt2[1];
            // sum of total distance
            return Math.sqrt(dist0 * dist0 + dist1 * dist1);
        },
        // calculates point that is dist from pt0 on line between pt0 to pt1
        interpBetwPts(pt1, pt0, dist) {
            // calc line and then get distance from first point
            const slope = (pt1[1] - pt0[1]) / (pt1[0] - pt0[0]);
            const b = pt0[1] - slope * pt0[0];
            const x1 = pt0[0] + dist / Math.sqrt(1 + (slope * slope));
            const y1 = slope * x1 + b;

            // calc in both directions on line
            const x2 = pt0[0] - dist / Math.sqrt(1 + (slope * slope));
            const y2 = slope * x2 + b;
            // compare distances from point 1
            const d1 = this.calcDistBetwPts([x1, y1], pt1);
            const d2 = this.calcDistBetwPts([x2, y2], pt1);
            // return the closer one to point 1 (e.g. between the two points)
            if (d1 <= d2) {
                return [x1, y1];
            }
            return [x2, y2];
        },
        // calculate the current coordinates of a bus between stop1 and stop2
        // Note this implementation assumes route segments are in order :/
        calcBusCoords(stop1, stop2, line, dtstr = '1/1/2000') {
            // put all times into arbitrary date so we can do math with them
            const curTime = new Date(dtstr + ' ' + this.time);
            const stop2arv = (stop2.arrival_time === '') ? new Date(dtstr + ' 00:00') : new Date(dtstr + ' ' + stop2.arrival_time);
            const stop1dept = (stop1.departure_time === '') ? new Date(dtstr + ' 23:59') : new Date(dtstr + ' ' + stop1.departure_time);
            const totalTime = stop2arv - stop1dept; // total time spent on route
            const timeSinceDept = curTime - stop1dept; // minutes since departing stop1
            const percTime = timeSinceDept / totalTime; // percentage of way bus is through segment
            
            const route = routesList.find((rt) => rt.lineAbbr === line); // route obj
            const scaledDist = percTime * route.path_length; // distance bus has gone on path

            let sumDist = 0;
            let d1 = 0;
            let extDist = 0;
            // sum distance between dept and arv coordinates, saving coords in between
            for (let i = 0; i < route.coordinates.length; i++) {
                // distance formula = sqrt((x2-x1)^2 + (y2-y1)^2)
                d1 = this.calcDistBetwPts(route.coordinates[i][1], route.coordinates[i][0]);

                // use length of summed segments to calculate the distance in map units bus should be from the start coordinate
                if (sumDist + d1 >= scaledDist) { // see if point should be on this line segment
                    extDist = scaledDist - sumDist; // distance to go on segment
                    return this.interpBetwPts(route.coordinates[i][1], route.coordinates[i][0], extDist); // route.coordinates[i][0];
                }
                sumDist += d1; // keep running total
            }
            return route.coordinates[0][0]; // if fails return stop1 coordinates
        },
    }

};

</script>

<style>
.left-align {
    text-align: left;
    padding:1em;
}
.time-slider {
    top:3px;
    min-height:vh;
    flex-shrink:0;
}
</style>
