/* eslint-disable max-len no-continue */
<template>
    <div>
        <div class="map">
            <BusMap /> 
        </div>
    </div>
</template>

<script>
import stopsList from '../data/allStops.json';
import routesList from '../data/allRoutes.json';
import BusMap from './BusMap.vue';

export default {
    name: 'MapPanel',
    components: {
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
        }
    },
    mounted: function () {
        const busLocs = this.calcBusLocations();
        this.$store.dispatch('changeBusLocations', busLocs);
    },
    methods: {
        geoJsonObj(busId, busCoordinates) {
            return { 
                type: 'Feature',
                properties: { 
                    id: busId
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
                    // if (bus.id !== '1000') {
                    //     continue;
                    // }

                    // if arv <= t <= dpt   -> at stop
                    if (arvtime <= curTime && curTime <= deptime) {
                        const stationObj = stopsList.find((station) => station.stopName === stp.stop_name);
                        // console.log('Here1', stp, stationObj);
                        
                        // TODO: add atStation if at charging station?
                        if (stationObj) {
                            busLocs.features.push(this.geoJsonObj(bus.id, stationObj.coordinates));
                            break;
                        }
                    // if dpt <= t <= next.arv   -> between stops.
                    } else if (deptime <= curTime && curTime <= nextArvtime) {
                        // calc coords
                        const coords = this.calcBusCoords(stp, bus.stops[i + 1], bus.line);
                        // console.log('Here2', coords, stp);
                        if (coords !== '') {
                            busLocs.features.push(this.geoJsonObj(bus.id, coords));
                            break;
                        }  
                    // t <= arv   -> usually means bus has not left the station for the day        
                    } else if (curTime <= arvtime) {
                        // console.log('Here3', stp);
                        const stationObj = stopsList.find((station) => station.stopName === stp.stop_name);
                        if (stationObj) {
                            busLocs.features.push(this.geoJsonObj(bus.id, stationObj.coordinates));
                            break;
                        }
                        break;
                    }
                }
            });
            return busLocs;
        },
        // calculate the current coordinates of a bus between stop1 and stop2
        calcBusCoords(stop1, stop2, line, dtstr = '1/1/2000') {
            const curTime = new Date(dtstr + ' ' + this.time);
            const stop2atime = (stop2.arrival_time === '') ? new Date(dtstr + ' 00:00') : new Date(dtstr + ' ' + stop2.arrival_time);
            const stop1dtime = (stop1.departure_time === '') ? new Date(dtstr + ' 23:59') : new Date(dtstr + ' ' + stop1.departure_time);
            const totalTime = stop2atime - stop1dtime;
            const route = routesList.find((rt) => rt.lineAbbr === line); // shape_length
            const curTimeMil = curTime - new Date(dtstr + ' :00:00');
            const scaledLen = (curTimeMil * route.path_length) / totalTime; // use time ratio to calc distance traveled

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
            console.log(sumDist, scaledLen);
            return '';
        },
        // // returns true if t1 is >= t2. Only for military time
        // timeIsGreaterEqTo(t1, t2) {
        //     const hr1 = parseInt(t1.split(':')[0], 10);
        //     const hr2 = parseInt(t2.split(':')[0], 10);
        //     if (hr1 > hr2) {
        //         return true;
        //     }
        //     if (hr2 > hr1) {
        //         return false;
        //     } // if equal hours
        //     const min1 = parseInt(t1.split(':')[1], 10);
        //     const min2 = parseInt(t2.split(':')[1], 10);
        //     if (min1 >= min2) { // if they're equal just say true
        //         return true;
        //     }
        //     return false;
        // }
    }

};

</script>

<style>
.left-align{
    text-align: left;
    padding:1em;
}
</style>
