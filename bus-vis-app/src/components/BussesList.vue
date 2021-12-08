/* eslint-disable no-confusing-arrow */
<template>
  <div>
    <ul id="busList">
        <li class="header">
            <div @click="sortBusses('busNo')">Bus No.</div> 
            <div @click="sortBusses('route')">Route</div> 
            <div @click="sortBusses('envEquity')">EnvEquity</div> 
            <div @click="sortBusses('battery')">Battery</div>
        </li>
        <li v-for="item in planBusses" 
            :key="item.id"
            :class="[item.id == selectedBus ? 'selected' : '', 'listItem']"
            @click="selectItem(item.id)"
        > 
            <div><i :class="[item.converted? '' : 'hidden', 'fas fa-plug']"></i>{{ item.id }}</div>
            <div>{{item.line}}</div>
            <div>{{item.environmental_equity}}</div>
            <div>{{getBatteryLevel(item.id)}}%</div>
        </li>
    </ul>
  </div>
</template>

<script>
// import stopsList from '../data/allStops.json';
import p20 from '../data/buses/p20.json';
import p60 from '../data/buses/p60.json';
import p180 from '../data/buses/p180.json';

export default {
    name: 'BussesList',
    props: {
        planObj: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            // 'converted' || 'envEquity' || 'route' || 'batteryLevel' || 'busNo'
            sortBy: 'converted',
            planBusses: this.getInitPlanBuses()
        };
    },
    computed: {
        busLocations: function () {
            return this.$store.state.busLocations;  
        },
        plan: function () {
            return this.$store.state.plan;
        },
        selectedBus: function () {
            return this.$store.state.selectedBus;
        },
    },
    methods: {
        getInitPlanBuses: function () {
            const bs = this.planObj;
            const s1 = this.sortByBusNo(bs.buses);
            return s1.sort((a, b) => (a.converted > b.converted) ? -1 : 1);
        },
        selectItem: function (busId) {
            this.$store.dispatch('changeBus', busId);
        },
        getBatteryLevel: function (busId) {
            if (this.busLocations.features.length <= 1) {
                return 0;
            }
            const bus = this.busLocations.features.find((b) => b.properties.id === busId.toString());
            if (bus.properties.converted) {
                return parseInt(bus.properties.remainingCharge, 10);
            }
            return 0; // if not converted don't show weird negative numbers
        },
        // sort busses by chosen method: 'converted' || 'envEquity' || 'route' || 'batteryLevel' || 'busNo'
        sortBusses: function (method) {
            let bl = this.planBusses;
            console.log(this.sortBy, method);
            if (method === this.sortBy) {
                console.log('reverse');
                // just reverse bus list TODO doesnt work
                bl.reverse();
            } else if (method === 'converted') {
                bl = this.planBusses.sort((a, b) => (a.converted > b.converted) ? -1 : 1);
            } else if (method === 'envEquity') {
                bl = this.planBusses.sort((a, b) => (a.environmental_equity > b.environmental_equity) ? 1 : -1);
            } else if (method === 'route') {
                bl = this.planBusses.sort((a, b) => (parseInt(a.line, 10) > parseInt(b.line, 10)) ? 1 : -1);
            } else if (method === 'battery') { // TODO
                bl = this.planBusses.sort((a, b) => (this.getBatteryLevel(a.id) > this.getBatteryLevel(b.id)) ? -1 : 1);
            } else if (method === 'busNo') {
                bl = this.planBusses.sort((a, b) => (a.id > b.id) ? 1 : -1);
            }
            this.sortBy = method;
            this.planBusses = bl;
        },

        sortByBusNo: function (busList) {
            return busList.sort((a, b) => (a.id > b.id) ? 1 : -1);
        },
        // sortByConverted: function (busList) {
        //     return busList.sort((a, b) => (a.converted > b.converted) ? -1 : 1);
        // },
        // sortByEnvEquity: function (busList) {
        //     return busList.sort((a, b) => (a.environmental_equity > b.environmental_equity) ? 1 : -1);
        // },
        // sortByBattery: function (busList) {
        //     //return busList.sort((a, b) => (a.battery_level > b.battery_level) ? 1 : -1);
        //     return busList.sort((a, b) => (a.converted > b.converted) ? -1 : 1);
        // },
        // sortByRoute: function (busList) {
        //     return busList.sort((a, b) => (a.route > b.route) ? -1 : 1);
        // },
    }
};

</script>

<style>
.header{
    font-size: smaller;
    display: flex;
    justify-content: space-between;
    /* padding: 0 0.6em; */
}
.header > div {
    padding: 0 0.6em;
}
.header > div:hover {
    background-color: #cdeceb;
}
.selected {
    color: white;
    background: lightseagreen !important;
}
ul#busList > li:nth-of-type(odd) {
    background-color: white;
}
.listItem{
    padding: 0.6em;
    text-align:left;
    display: flex;
    justify-content: space-between;
}
.hidden{
    visibility: hidden;
}

</style>
