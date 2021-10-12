/* eslint-disable max-len no-continue */
<template>
    <div class="MAP"> {{ busLocations[0] }}
    </div>
</template>

<script>

import p20 from '../data/buses/p20.json';
import stopsList from '../data/allStops.json';
import routesList from '../data/allRoutes.json';

export default {
    name: 'MapPanel',
    props: {
        planBusses: {
            type: Object
        },
    },
    computed: {
        time: function () {
            return this.$store.state.time;
        },
        // returns array of {busID: ID, coordinates: [lat,long]}
        busLocations: function () { 
            const busLocations = [];
            p20.buses.forEach((bus) => {
                for (let i = 0; i < bus.stops.length; i++) {
                    const stp = bus.stops[i];
                    // if arv <= t <= dpt  -> at stop
                    const stpatime = (stp.arrival_time === '') ? '00:00' : stp.arrival_time;
                    if ((this.timeIsGreaterEqTo(this.time, stpatime) && this.timeIsGreaterEqTo(stp.departure_time, this.time)) || stp.departure_time === '') {
                        const stationObj = stopsList.find((station) => station.stopName === stp.stop_name);
                        if (stationObj) {
                            busLocations.push({ busID: bus.id, coordinates: stationObj.coordinates });
                            break;
                        }
                    // if dpt <= t <= next.arv  -> between stops
                    } else if (this.timeIsGreaterEqTo(this.time, stp.departure_time) && this.timeIsGreaterEqTo(bus.stops[i + 1].arrival_time, this.time)) {
                        // calc coords
                        const coords = this.calcBusCoords(stp, bus.stops[i + 1], bus.line);
                        if (coords !== '') {
                            busLocations.push({ busID: bus.id, coordinates: coords });
                            break;
                        }             
                    } else if (this.timeIsGreaterEqTo(stpatime, this.time)) {
                        break;
                    }
                }
            });
            return busLocations;
        }
    },
    methods: {
        // calculate the current coordinates of a bus between stop1 and stop2
        calcBusCoords(stop1, stop2, line) {
            const stop2atime = (stop2.arrival_time === '') ? '00:00' : stop2.arrival_time;
            const totalTime = stop2atime - stop1.departure_time;
            const route = routesList.find((rt) => rt.lineAbbr === line); // shape_length
            const scaledLen = (this.time * route.shape_len) / totalTime; // use time ratio to calc distance traveled
            
            let sumDist = 0;
            for (let i = 0; i < route.coordinates.length; i++) {
                if (i === 0) {
                    continue;
                }
                // calc distance between two points
                const dist0 = route.coordinates[i - 1][0] - route.coordinates[i][0];
                const dist1 = route.coordinates[i - 1][1] - route.coordinates[i][1];
                // sum of total distance
                sumDist += Math.sqrt(dist0 * dist0 + dist1 * dist1);
                if (sumDist >= scaledLen) {
                    return route.coordinates[i];
                }
            }
            return '';
        },
        // returns true if t1 is >= t2
        timeIsGreaterEqTo(t1, t2) {
            const hr1 = parseInt(t1.split(':')[0], 10);
            const hr2 = parseInt(t2.split(':')[0], 10);
            if (hr1 > hr2) {
                return true;
            }
            if (hr2 > hr1) {
                return false;
            } // if equal hours
            const min1 = parseInt(t1.split(':')[1], 10);
            const min2 = parseInt(t2.split(':')[1], 10);
            if (min1 >= min2) { // if they're equal just say true
                return true;
            }
            return false;
        }
    }

};

</script>

<style>
.left-align{
    text-align: left;
    padding:1em;
}

</style>
