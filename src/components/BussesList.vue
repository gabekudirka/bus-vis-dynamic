/* eslint-disable no-confusing-arrow */
<template>
  <div>
    <ul id="busList">
        <li class="header">
            <input type="checkbox" v-model="allOn" @change="checkAll()" style="margin:0 0.6em"/>
            <div @click="sortBusses('busNo')">Bus No.</div> 
            <div @click="sortBusses('route')">Line</div> 
            <div @click="sortBusses('envEquity')">Env. Equity</div> 
            <div @click="sortBusses('battery')">Battery</div>
        </li>
        <li v-for="item in planBusses" 
            :key="item.id"
            :class="[item.id == selectedBus ? 'selected' : '', 'listItem']"
            @click="selectItem(item.id)"
        > 
            <input type="checkbox" name="check" checked="true" @change="checkOne(item.id)"/>
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
            planBusses: this.getPlanBuses(),
            allOn: true
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
        bussesToShow: function () {
            return this.$store.state.bussesToShow;
        },
        routeFocused: function () {
            return this.$store.state.routeFocused;
        }
    },
    watch: {
        bussesToShow: function () {
            this.planBusses = this.getPlanBuses();
        },
    },
    methods: {
        checkAll: function () {
            // toggle show for all busLocations
            if (this.routeFocused) {
                this.busLocations.features.forEach(bus => {
                    if (this.bussesToShow.includes(bus.properties.id)) {
                        bus.properties.show = this.allOn;
                    }
                });
            } else {
                this.busLocations.features.forEach(bus => {
                    bus.properties.show = this.allOn;
                });
            }
            
            // toggle all checkboxes
            document.getElementsByName('check').forEach(checkbox => {
                checkbox.checked = this.allOn;
            });
            // update the state
            this.$store.dispatch('changeBusLocations', this.busLocations);
        },
        checkOne: function (busId) {
            // toggle the show property for given busID
            const bus = this.busLocations.features.find((b) => b.properties.id === busId.toString());
            bus.properties.show = !bus.properties.show;
            if (!bus.properties.show) {
                this.allOn = false;
            }
            // update state
            this.$store.dispatch('changeBusLocations', this.busLocations);
        },
        getPlanBuses: function () {
            let bs = this.planObj.buses;
            if (this.bussesToShow != null) {
                bs = [];
                this.bussesToShow.forEach(busId => {
                    bs.push(this.planObj.buses.find(bus => bus.id === busId));
                });
            }
            const s1 = this.sortByBusNo(bs);
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
            if (bus && bus.properties.converted) {
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
    }
};

</script>

<style>
.header{
    font-size: smaller;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: bold;
    border-bottom: 2px solid #cdeceb;
    /* border-top: 2px solid #cdeceb; */
    /* padding: 0.6em; */
    /* padding: 0 0.6em; */
}
.header > div {
    padding: 0 0.6em;
    height:100%;
    height: 35px;
    display: flex;
    align-items: center;
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
    align-items: center;
}
.hidden{
    visibility: hidden;
}

</style>
