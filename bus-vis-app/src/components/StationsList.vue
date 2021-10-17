<template>
  <div>
    <ul id="stationsList">
        <li v-for="item in planStations" 
            :key="item.stop_id"
            :class="[item.stop_id == selectedStation ? 'selected' : '', 'listItem']"
            @click="selectItem(item.stop_id)"
        >
            {{ item.stop_name }} {{ item.stop_id}}
        </li>
    </ul>
  </div>
</template>

<script>
import stopsList from '../data/allStops.json';

export default {
    name: 'StationsList',
    data() {
        return {
            stops: stopsList,
        };
    },
    props: {
        planObj: {
            type: Object,
            required: true
        }
    },
    computed: {
        plan: function () {
            return this.$store.state.plan;
        },
        selectedStation: function () {
            return this.$store.state.selectedChargingStation;
        },
        planStations: function () {
            return this.planObj.charging_stations;
        },
        // selectedStation: function () {
        //     // find the stop
        //     const stp = stopsList.find((stop) => stop.stopId === this.stationID);
        //     // find the charging station object 
        //     const chStation = this.planStations.find((station) => station.stop_name === stp.stopName);
        //     // if no charging station, just return stop
        //     if (!chStation) {
        //         return stp;
        //     }
        //     // else return concatenated object
        //     return { ...chStation, ...stp, converted: true };
        // }
    },
    methods: {
        selectItem: function (stopId) {
            this.$store.dispatch('changeStation', stopId);
        }
    }
};

</script>

<style>
.selected {
    color: white;
    background: lightseagreen !important;
}
ul#stationsList > li:nth-of-type(odd) {
    background-color: white;
}
.listItem{
    padding: 0.6em;
    text-align:left;
}

</style>
