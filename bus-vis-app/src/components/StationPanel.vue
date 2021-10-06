/* eslint-disable max-len */
<template>
    <div class="left-align">
        <h4>Station: {{selectedStation.StopId}} </h4>
        <p>Located at: {{selectedStation.StopName}} </p>
        <p>Busses currently @ station: bus2, bus5, bus8</p>
        <p>Current station power output: 3000 powers </p>
        <p>Busses visited station so far: 5/23 </p>
    </div>
</template>

<script>
import p20 from '../data/plans/p20.json';
import p60 from '../data/plans/p60.json';
import p180 from '../data/plans/p180.json';

import stopsList from '../data/allStops.json';

export default {
    name: 'StationPanel',
    props: {
        // plan: {
        //     type: String,
        //     required: true
        // },
        // stationID: {
        //     type: Number,
        //     required: true
        // }
    },
    computed: {
        plan: function () {
            return this.$store.state.plan;
        },
        stationID: function () {
            return this.$store.state.selectedChargingStation;
        },
        planStations: function () {
            if (this.plan === 'p20') {
                console.log(p20.charging_stations);
                return p20.charging_stations;
            } if (this.plan === 'p80') {
                return p60.charging_stations;
            }
            return p180.charging_stations;
        },
        stations: function () {
            const list = [];
            this.planStations.forEach((station) => {
                const st = stopsList.find((stop) => stop.StopName === station.stop_name);
                // TODO: use filter?? Multiple stops with same name but diff ids...
                list.push({ ...station, ...st, converted: true });
            });
            console.log(list);
            return list;
        },
        selectedStation: function () {
            // try to find a charging station @ stop
            let st = this.stations.find((station) => station.StopId === this.stationID);
            // otherwise just show stop info
            if (!st) {
                st = stopsList.find((stop) => stop.StopId === this.stationID);
            }
            console.log('here');
            console.log(st);
            return st;
        }
    },

};

</script>

<style>
.left-align{
    text-align: left;
    padding:1em;
}
p{
    margin-bottom:0.5em !important;
}
</style>
