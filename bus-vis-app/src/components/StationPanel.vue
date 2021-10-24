/* eslint-disable max-len prefer-destructuring */
<template>
    <div class="left-align">
        <div style="padding:1em">
            <h4>
                <i class="fas fa-charging-station"></i>
                {{selectedStation.stopName}} 
            </h4>
            <div class="sidebyside">
                <div class="stationInfo">
                    <p> <b> UTA Stop: </b> <br> {{selectedStation.stopId}} </p>
                    <p> <b> Buses @ Station: </b> </p>
                    <p v-for="bus in bussesAtStation" :key="bus" class="busnum">
                        {{bus}}
                    </p>
                    <p> <b> Current Power Output: </b> <br> {{ bussesAtStation.length * powerOutPerBus}} </p>
                </div>
                <div class="flex1">
                    <div v-show="selectedStation.converted" id="charge-chart-container" class="chart">
                        <p class="chart-title"> <b> Num Buses @ Station </b> </p>
                        <PanelChart
                            :key="stationChartData"
                            :data="stationChartData"
                            :chartName="'stations-chart'"
                            :containerWidth="chartSize.width"
                            :containerHeight="chartSize.height"
                        />
                    </div>
                </div>
             </div>
        </div>
    </div>
</template>

<script>

import PanelChart from './PanelChart.vue';
import stopsList from '../data/allStops.json';
import busesAtStations from '../data/BusesAtStations.json';

export default {
    name: 'StationPanel',
    components: {
        PanelChart,
    },
    props: {
        planObj: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            powerOutPerBus: 1, // TODO: figure out number
            chartSize: {
                height: 210,
                width: 400
            }
        };
    },
    computed: {
        stationID: function () {
            return this.$store.state.selectedChargingStation;
        },
        planStations: function () {
            return this.planObj.charging_stations;
        },
        selectedStation: function () {
            // find the charging station object 
            let chStation = this.planStations.find((station) => station.stop_id === this.stationID);
            // if we can't find the station, return the first one of the plan
            if (!chStation) {
                chStation = this.planStations[0];
            }
            // find the stop
            const stp = stopsList.find((stop) => stop.stopName === chStation.stop_name);
            return { ...chStation, ...stp, converted: true };
        },
        busLocations: function () {
            return this.$store.state.busLocations;
        },
        bussesAtStation: function () {
            // find all busses at same locations
            // busLocations show up as proxy object (figure out why) so we have to check each coordinate seperatesly
            const busses = this.busLocations.features.filter((bus) => (bus.geometry.coordinates[0] === this.selectedStation.coordinates[0]) 
                                                            && (bus.geometry.coordinates[1] === this.selectedStation.coordinates[1]));
            return busses.map((b) => b.properties.id);
        },
        // TODO: FINISH
        stationChartData: function () {
            const data = busesAtStations[this.selectedStation.stop_name];
            console.log('stData', data.busTimes);
            const stationData = [];
            Object.keys(data.busTimes).forEach((time) => {
                stationData.push({ x: time, y: data.busTimes[time].length });
            });
            console.log(stationData);
            return stationData;
        },
    },
};

</script>

<style>
/* .left-align{
    text-align: left;
    padding:1em;
} */
p{
    margin: 0.2em !important;
}
.sidebyside {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: space-between;
}
.flex1 {
    flex: 1;
    padding: .2em;
}
.busnum {
    display: inline-block;
}
.stationInfo{
    max-width:30vw;
    margin-right:1em;
}
.chart{
    max-width:40vw;
}

</style>
