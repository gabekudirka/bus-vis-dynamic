/* eslint-disable max-len prefer-destructuring */
<template>
    <div class="left-align">
        <h4>
            <i class="fas fa-charging-station"></i>
             {{selectedStation.stopName}} 
        </h4>
        <div class="sidebyside">
            <table id="stationInfo" class="flex1">
                <tr>
                    <td> UTA Stop ID </td>
                    <td> {{selectedStation.stopId}} </td>
                </tr>
                <tr> 
                    <td>Busses @ Station </td>
                    <td class="sidebyside">
                        <div v-for="bus in bussesAtStation" :key="bus" class="busnum">
                            {{bus}}
                        </div>
                    </td>
                </tr>
                <tr>
                    <td> Current Power Output </td>
                    <td> {{ bussesAtStation.length * powerOutPerBus}} </td>
                </tr>
            </table>    
            <div class="flex1"> <TimeSlider /> </div>
            <div class="flex1"> PUT CHART2 HERE </div>
        </div>
    </div>
</template>

<script>
import TimeSlider from './TimeSlider.vue';
import stopsList from '../data/allStops.json';

export default {
    name: 'StationPanel',
    components: {
        TimeSlider,
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
        };
    },
    computed: {
        stationID: function () {
            return this.$store.state.selectedChargingStation;
        },
        planStations: function () {
            return this.planObj.charging_stations;
        },
        // stations: function () {
        //     const list = [];
        //     this.planStations.forEach((station) => {
        //         const st = stopsList.find((stop) => stop.stopName === station.stop_name);
        //         // TODO: use filter?? Multiple stops with same name but diff ids...
        //         list.push({ ...station, ...st, converted: true });
        //     });
        //     console.log(list);
        //     return list;
        // },
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

            // // try to find a charging station @ stop
            // let st = this.stations.find((station) => station.stopId === this.stationID);
            // // otherwise just show stop info
            // if (!st) {
            //     st = stopsList.find((stop) => stop.stopId === this.stationID);
            // }
            // console.log('here');
            // console.log(st);
            // return st;
        },
        busLocations: function () {
            return this.$store.state.busLocations;
        },
        bussesAtStation: function () {
            // find all busses at same locations
            // busLocations show up as proxy object (figure out why) so we have to check each coordinate seperatesly
            const busses = this.busLocations.features.filter((bus) => (bus.geometry.coordinates[0] === this.selectedStation.coordinates[0]) 
                                                            && (bus.geometry.coordinates[1] === this.selectedStation.coordinates[1]));
            return busses.map((b) => b.busID);
        }
    },
};

</script>

<style>
.left-align{
    text-align: left;
    padding:.6em;
}
p{
    margin: 0.2em !important;
}
.sidebyside {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
}
.flex1 {
    flex: 1;
    padding: .2em;
}
.busnum {
    padding:0 .1em;
}
#stationInfo{
    border: 1px solid #efefef;
}
#stationInfo > tr > td:first-child{ 
    font-weight: bold;
    background-color: #efefef;
    border-bottom: 1px solid white;
}
td {
    padding: 0.2em;
    border-bottom: 1px solid #efefef;
}

</style>
