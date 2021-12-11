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
        plan: function () {
            return this.$store.state.plan;
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
        plan: function () {
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
        // calculate the current coordinates of a bus between stop1 and stop2
        calcBusCoords(stop1, stop2, line, dtstr = '1/1/2000') {
            const curTime = new Date(dtstr + ' ' + this.time);
            const stop2atime = (stop2.arrival_time === '') ? new Date(dtstr + ' 00:00') : new Date(dtstr + ' ' + stop2.arrival_time);
            const stop1dtime = (stop1.departure_time === '') ? new Date(dtstr + ' 23:59') : new Date(dtstr + ' ' + stop1.departure_time);
            const totalTime = stop2atime - stop1dtime;
            const route = routesList.find((rt) => rt.lineAbbr === line); // shape_length
            const curTimeMil = curTime - new Date(dtstr + ' :00:00');
            
            // const station1 = stopsList.find((station) => station.stopName.replace(/\s/g, '') === stop1.stop_name.replace(/\s/g, ''));
            // const station2 = stopsList.find((station) => station.stopName.replace(/\s/g, '') === stop2.stop_name.replace(/\s/g, ''));
            // const segmentLen = this.calcDistBetwPts(station1.coordinates, station2.coordinates);
            // const scaledLen = (curTimeMil * segmentLen) / totalTime; // use time ratio to calc distance traveled
            // TODO this should be distace between two station coordinates

            const scaledLen = (curTimeMil * route.path_length) / totalTime;

            // sum distance between each stop until we reach the distance traveled, then return those coordinates
            let sumDist = 0;
            for (let i = 0; i < route.coordinates.length; i++) {
                if (i === 0) {
                    continue;
                }
                // calc distance between two points
                // TODO: why are route coords [[l,lg],[l,lg]] ???
                const dist0 = route.coordinates[i][0][0] - route.coordinates[i - 1][0][0];
                const dist1 = route.coordinates[i][0][1] - route.coordinates[i - 1][0][1];
                // sum of total distance
                sumDist += Math.sqrt(dist0 * dist0 + dist1 * dist1);
                if (sumDist >= scaledLen) {
                    return route.coordinates[i][0];
                }
            }
            return '';
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
