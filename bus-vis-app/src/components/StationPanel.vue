/* eslint-disable max-len */
<template>
  <div>{{stations}}</div>
</template>

<script>
import p20 from '../data/plans/p20.json';
import p60 from '../data/plans/p60.json';
import p180 from '../data/plans/p180.json';

import stopsList from '../data/allStops.json';

export default {
    name: 'BusPanel',
    props: {
        plan: {
            type: String,
            required: true
        },
        stationID: {
            type: String,
            required: true
        }
    },
    // data() {
    //     return {
    //         stops: stopsList
    //     };
    // },
    computed: {
        planStations: function () {
            if (this.plan === 'A') {
                return p20.charging_stations;
            } if (this.plan === 'B') {
                return p60.chargin_stations;
            }
            return p180.charging_stations;
        },
        stations: function () {
            const list = [];
            this.planStations.forEach((station) => {
                stopsList.forEach((stp) => {
                    // console.log(station.stop_id, stp.StopId);
                    if (station.stop_name === stp.StopName) {
                        list.add({ ...station, ...stp });
                        // break;
                    }
                });
            });
            // for (station in Object.values(planStations)) {
            //     for (stp in Object.values(stopsList)){
            //         if (station.stop_id == stop.StopId){
            //             list.append({...station, ...stp });
            //             break;
            //         }
            //     }
            // }
            console.log(list);
            return list;
        }
    },
    // methods: {
    //     jsonToDict(jsonData) {
    //         const buses = {};
    //         const busData = jsonData;
    //         for (let i = 0; i < busData.buses.length; i++) {
    //             const bus = busData.buses[i];
    //             buses[bus.id] = bus;
    //         }
    //         return buses;
    //     }
    // }
};

</script>

<style>

</style>
